## To Do

- Front end for street stats generation
- Possibly refactor so that instead of bounding boxes, we can use nodes inside way 
- Blog post: Adventures in setting up an interactive data tool for the first time
    > Blog post. Entire journey. Explain stack, problems, why I chose to do somethings, even if its dumb. If anything, it's a historical reference for myself.
    * [ ] Intro, how I found the data, why I want to look at it
    * [ ] How did I get the data. What stack? From where?
    * [ ] How did I parse the data? Using what tools? 
    * [ ] Why did I set up a nominatim server
    * [ ] Why did I set up a openmaptile server
    * [ ] Why I don't need both
    * [ ] Why did the web part take so long? New to django, web dev in general. Started with Flask but moved to django. Why?
    * [ ] Ouchy in data: Julia serialized DateTime unreadable inpython
    * [ ] Realizing server / client would explode if had to do computations every time they clicked on a street segment
    * [ ] Loading data is slow as hell. Possible fixes: MySQL, django
    * [ ] 

## In progress

- Set up osm-website on cloud.csclub
    > Notes: Failed at using vagrant and docker, so now its time to install from scratch.
    * [x] Download toronto.osm
    * [x] import database (?)
- Back end for street stats generation
    * [ ] Query all infractions
    * [ ] Mean, mode, top time of day, ranking?, interarrival time
    * [ ] how to do nice graphs and shit
- Revamp database, in the meantime probably add to django
    > Fucked up database cause python cant read datetime, and realized that calculating interarrivals will probably destroy caffeine and / or client.
    * [ ] Use julia to convert 'proprietary' datetime in to string for interconvertability
    * [ ] For each osm_id add exponential fit, mean, etc

## Done

