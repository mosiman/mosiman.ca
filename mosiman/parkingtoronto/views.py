from django.shortcuts import render
from django.template import loader
from django.http import HttpResponse, JsonResponse
import sqlite3


# Create your views here.

def index(request):
    template = loader.get_template('parkingtoronto/index.html')
    return render(request, 'parkingtoronto/index.html')

def streetsegapi(request):
    lat = request.POST['lat']
    lng = request.POST['lng']
    outstring = str(lat) + ", " + str(lng) + " is "

    conn = sqlite3.connect('allstreetsegs.db')
    c = conn.cursor()

    c.execute('select * from streetsegments where (? between slat and nlat) and (? between wlng and elng)', (str(lat), str(lng)))

    ss_result = c.fetchone()

    if ss_result:
        # format: [osm_id, name, slat, nlat, wlng, elng]
        outstring += "inside way: " + str(ss_result[0])
        bbox = ss_result[2:]

        return JsonResponse({
            'outstring': outstring,
            'found': True,
            'bbox': bbox })
    else:
        return JsonResponse({
            'outstring': outstring + "not inside any bbox in db",
            'found': False,
            'bbox': [] })
