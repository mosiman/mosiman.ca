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

    # try finding the entry, else, return to previous page
    try:
        # get entry where slug is the same
        entry = Entry.objects.get(slug=slug)
        # load that into contents variable

        context = {
                'entry': entry
                }
        template = loader.get_template('blog/post.html')
        return HttpResponse(template.render(context))

        # HttpResponse return the markdownified html
    except Exception as e:
        print(e)
        # actually should 404
        return HttpResponse(loader.get_template('blog/index.html'))

