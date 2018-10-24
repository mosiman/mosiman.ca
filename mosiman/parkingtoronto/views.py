from django.shortcuts import render
from django.template import loader, RequestContext
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import ensure_csrf_cookie
import sqlite3


# Create your views here.

@ensure_csrf_cookie
def index(request):
    template = loader.get_template('parkingtoronto/index.html')
    return render(request, 'parkingtoronto/index.html')


def streetsegapi(request):
    print("wassup")
    lat = request.POST['lat']
    lng = request.POST['lng']
    outstring = str(lat) + ", " + str(lng) + " is "

    conn = sqlite3.connect('allstreetsegs.db')
    c = conn.cursor()

    c.execute('select * from streetsegments where (? between slat and nlat) and (? between wlng and elng)', (str(lat), str(lng)))

    ss_result = c.fetchone()

    if ss_result:
        # format: [osm_id, name, slat, nlat, wlng, elng, explambda, numtickets]
        outstring += "inside way: " + str(ss_result[0])
        bbox = ss_result[2:6]

        # get all infractions from way

        c.execute('select * from streetsegmentinfractions where osm_id = ?', (str(ss_result[0]),))
        infs = c.fetchall()
        colnames = [d[0] for d in c.description]
        infarr = []
        for row in infs:
            infdict = dict(zip(colnames, row))
            infarr.append(infdict)
            # thanks https://stackoverflow.com/a/9986400/5146008
        print(len(infs))

        nodearr = []
        c.execute('select * from waynodes where osm_id = ? order by nodeorder asc', (str(ss_result[0]),))
        nodes = c.fetchall()
        colnames = [d[0] for d in c.description]
        print("numnodes:")
        print(len(nodes))
        for row in nodes:
            nodedict = dict(zip(colnames, row))
            nodearr.append(nodedict)

        return JsonResponse({
            'outstring': outstring,
            'name': ss_result[1],
            'found': True,
            'bbox': bbox,
            'infs': infarr,
            'nodes': nodearr,
            'explambda': ss_result[6],
            'numtickets': ss_result[7]})
    else:
        return JsonResponse({
            'outstring': outstring + "not inside any bbox in db",
            'name': '',
            'found': False,
            'bbox': [] })
