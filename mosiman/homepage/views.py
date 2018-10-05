from django.shortcuts import render
from django.template import loader
from django.http import HttpResponse

from .models import PortfolioPiece

# Create your views here.

def index(request):
    template = loader.get_template('homepage/index.html')
    portfoliopieces = PortfolioPiece.objects.all()

    context = { 'portfoliopieces': portfoliopieces }
    return render(request, 'homepage/index.html', context)
