from django.shortcuts import render
from django.template import loader
from django.http import HttpResponse, JsonResponse


# Create your views here.

def index(request):
    template = loader.get_template('parkingtoronto/index.html')
    return render(request, 'parkingtoronto/index.html')

def streetsegapi(request):
    #someint = request.args.get('somenum', -1, type=int)
    print(request)
    someint = request.POST['somenum']
    print(someint)
    return JsonResponse({'result': someint})
