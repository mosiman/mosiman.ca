from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader

from .models import Entry

# Create your views here.

def index(request):
    template = loader.get_template('blog/index.html')
    entries = Entry.objects.all()
    context = {
            'entries' : entries
            }
    return HttpResponse(template.render(context))

def blogpost(request, slug):
    # get entry where slug is the same

    # load that into contents variable

    # markdownify (don't forget the extensions!)

    # HttpResponse return the markdownified html
    return HttpResponse(slug)

