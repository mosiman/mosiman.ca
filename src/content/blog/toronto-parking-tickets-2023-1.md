---
title: 'Parking ticket visualization: data cleaning'
date: 2024-02-06
---

**tl;dr**: I located the street of each parking ticket to do analysis on a per-street basis. You can play with the dataset via the DuckDB WASM shell:

[DuckDB shell](https://shell.duckdb.org/#queries=v0,install-spatial~-load-spatial~%0A%0Acreate-table-parking_tickets-as%0Aselect%0A----infraction_ts%2C%0A----infraction_code%2C%0A----infraction_description%2C%0A----set_fine_amount%2C%0A----location1%2C%0A----location2%2C%0A----location3%2C%0A----location4%2C%0A----way_id%2C%0A----ST_GeomFromGeoJSON(way_geom)-as-way_geom%2C%0A----name%0Afrom-'https%3A%2F%2Fpub%20f6beeb64145748619c244838afe14b58.r2.dev%2Fparkingtickets.parquet'~%0A)

The link above will run the following commands on startup. The file is about 75 MB and will take a few seconds to load depending on your network speed.

```
install spatial; load spatial;

create table parking_tickets as
select
    infraction_ts,
    infraction_code,
    infraction_description,
    set_fine_amount,
    location1,
    location2,
    location3,
    location4,
    way_id,
    ST_GeomFromGeoJSON(way_geom) as way_geom,
    name
from 'https://pub-f6beeb64145748619c244838afe14b58.r2.dev/parkingtickets.parquet';
```

Notes about the DuckDB shell: 
- `select * from parking_tickets` doesn't work on my own machine, I suspect because the dataset is somewhat large. You should qualify the query with filters or a limit clause to avoid crashing the tab.
- Copying / pasting doesn't seem to work in Firefox. It works fine on Chrome, though. [Open issue](https://github.com/duckdb/duckdb-wasm/issues/1016).

Example query: Pull up the parking tickets for the way (street segment) closest to the given coordinates by hour:

```
with get_closest_way as (
    select
        name,
        way_id,
        ST_Distance(way_geom, ST_Point(-79.362650, 43.659153)) as distance
    from parking_tickets
    order by distance
    limit 1
)
select
    name,
    way_id,
    date_part('hour', infraction_ts) as hour,
    count(*) as num_tickets
from parking_tickets
where way_id = (select way_id from get_closest_way)
group by name, way_id, hour
order by hour;
```

--- 

# Toronto Parking Ticket Visualization (2023) - Part 1

This is the first post in a series of posts about analyzing and visualizing parking ticket data from the city of Toronto. This first post will be about cleaning the original dataset and augmenting it.

## The original dataset

The original dataset comes from the City of Toronto's [Open Data Portal](https://open.toronto.ca/dataset/parking-tickets/).

The data is stored in CSV files with the following format:

| Column Name             | Description                                            |
|-------------------------|--------------------------------------------------------|
| TAG_NUMBER_MASKED       | First three (3) characters masked with asterisks       |
| DATE_OF_INFRACTION      | Date the infraction occurred in YYYYMMDD format       |
| INFRACTION_CODE         | Applicable Infraction code (numeric)                   |
| INFRACTION_DESCRIPTION  | Short description of the infraction                    |
| SET_FINE_AMOUNT         | Amount of set fine applicable (in dollars)             |
| TIME_OF_INFRACTION      | Time the infraction occurred in HHMM format (24-hr clock) |
| LOCATION1               | Code to denote proximity (see table below)             |
| LOCATION2               | Street address                                         |
| LOCATION3               | Code to denote proximity (optional)                    |
| LOCATION4               | Street address (optional)                              |
| PROVINCE                | Province or state code of vehicle licence plate        |

The proximity code `LOCATION1` is additional information about the location of the infraction in relation to the provided address `LOCATION2`. Similar for `LOCATION3` and `LOCATION4`. Since a number of tickets (around 20%) are located not by an exact address, but by these additional location qualifiers, we will do our best to incorporate those tickets.

| Proximity Code | Description |
|----------------|-------------|
| AT             | At          |
| NR             | Near        |
| OPP            | Opposite     |
| R/O            | Rear of      |
| N/S            | North Side   |
| S/S            | South Side   |
| E/S            | East Side    |
| W/S            | West Side    |
| N/O            | North of     |
| S/O            | South of     |
| E/O            | East of      |
| W/O            | West of      |


## Data pipeline overview

The first step is to extract the `csv` files from the raw zip file provided by the open data portal. We'll use `duckdb` to read these.

```sql
select * from read_csv('Parking_Tags_Data_2022.*.csv', delim=',', header = true, quote='"', auto_detect=true, filename=true);
```

The analysis I want to do on this dataset requires geocoding the locations of the tickets at a "street" level. This service is offered by many providers, but to cut down on cost, we'll self host our own.

The `OpenStreetMap` project allows you to geocode for free, but it wouldn't be very nice of us to hammer their servers with a bulk request like this. Instead, we can make use of the docker container provided by [mediagis](https://github.com/mediagis/nominatim-docker)

The details are provided in `svc/nominatim/start.sh`. It's pretty straightforward, and the only thing of note here is that we're using a small `pbf` file only covering Toronto, which is graciously hosted by [BBBike](https://download.bbbike.org/osm/bbbike/Toronto/Toronto.osm.pbf)

The other piece of infrastructure we're going to stand up is a small server to host [libpostal](https://github.com/openvenues/libpostal), which is used to normalize street addresses. Similarly, the details are provided in `svc/libpostal_rest/start.sh`. I could have embedded this, but I didn't want to go through the effort to be frank. I opted for a [docker container](https://github.com/johnlonganecker/libpostal-rest) that someone else had built.


Once `nominatim` is up and running, you can issue requests like this:

```
❯ time curl 'http://localhost:8080/search.php?q=convocation%20hall'
[{"place_id":579324,"licence":"Data © OpenStreetMap contributors, ODbL 1.0. https://osm.org/copyright","osm_type":"way","osm_id":330718925,"boundingbox":["43.6605236","43.6610283","-79.3957883","-79.3951072"],"lat":"43.66077185","lon":"-79.3954329541008","display_name":"Convocation Hall, 31, King's College Circle, Discovery District, University—Rosedale, Old Toronto, Toronto, M5S 1A1, Canada","place_rank":30,"category":"place","type":"house","importance":0.20000999999999997}]
real	0m0.047s
user	0m0.004s
sys	0m0.001s
```

Unfortunately, we can't feed it the "intersection" data (those tickets located by `LOCATION1` and `LOCATION3`) as-is, so we'll need to do extra work there.

### Intersections

The `nominatim` API doesn't seem to allow for querying intersections from what I found, so we'll dig a bit deeper into the database.

A "way" is a collection of nodes. Streets are segmented by ways (lines) but buildings can also be represented by a way (polygon). According to [this answer](https://help.openstreetmap.org/questions/9344/how-to-detect-intersection-of-ways), ways that intersect _should_ have an intersecting node.

> If two streets intersect and neither of them is a bridge or tunnel, then they should have an intersection node; editors and validators will complain if they haven't.

For example: consider `University Ave and Queen St W`. This is how it's presented in the original dataset (`UNIVERSITY AVE`, `QUEEN ST W`) but we'll use `libpostal` to normalize that to `University Avenue` and `Queen Street West`.

```sql
WITH university_ways as (
    select
        p.osm_id,
        p.name,
        w.nodes,
        w.tags
    from place p
    left join planet_osm_ways w
        on w.id = p.osm_id
    where p.class = 'highway' and p.osm_type = 'W' and p.name['name'] = 'University Avenue'
), queen_ways as (
    select
        p.osm_id,
        p.name,
        w.nodes,
        w.tags
    from place p
    left join planet_osm_ways w
        on w.id = p.osm_id
    where p.class = 'highway' and p.osm_type = 'W' and p.name['name'] = 'Queen Street West'
), intersection as (
    select
        u.osm_id as u_osm_id,
        u.name as u_name,
        u.nodes as u_nodes,
        u.tags as u_tags,
        q.osm_id as q_osm_id,
        q.name as q_name,
        q.nodes as q_nodes,
        q.tags as q_tags
    from university_ways u
    join queen_ways q
        on u.nodes && q.nodes
)
select * from intersection
;
```

This returns a number of ways that intersect with the name "University Avenue" and "Queen Street West". We use the `LOCATION`, `LOCATION3` columns to locate which way based on the geometry.

With this, I am able to geocode most tickets either via the REST API, or through the database. The `hydrate.py` script shows this in greater detail.

I initially didn't set up a cache, but that would have helped out a lot. The `hydrate.py` script took 109 hours to run, almost 5 days.

My main goal with this dataset is to show "interarrival times" of a parking enforcement officer, as the distribution would show how likely an officer is to arrive within the next `X` minutes. The next steps are:

- Use a rolling window to calculate interrarival times (e.g.: a string of 5 tickets counts as "one arrival" if the tickets all occur in a short time period (say 15 minutes).
- Serve this data along with other general statistics (number of tickets by hour, most frequent ticket types via an API (or maybe force the client to download the 70mb parquet file, and do all the analytics on the client?)
- Visualize the statistics with Plotly and Leaflet.js.

---

Update (2024-03-08): I knew that hosting the parquet file on Github by including it in the git repository was a bad idea, but I didn't know of any decent services to host the file without incurring egress fees (my VPSes have limited bandwidth). I realized that Cloudflare R2 would host it for free, and without egrees fees. It's rate-limited, but its pretty much exactly what I need right now. I nuked that file from my repository and adjusted the links to pull the file from R2.
