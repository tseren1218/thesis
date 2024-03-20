from django.shortcuts import render
from django.views import generic
from .models import *
# Create your views here.

def index(request):
    return render(request, "core/index.html")

def get_locations(request):
    # print(Province.nodes.all())
    return render(request, 'core/locations.html', {'locations': Location.nodes.all()})

