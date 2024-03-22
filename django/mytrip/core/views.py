from datetime import timezone
from django.shortcuts import redirect, render

from core.forms import ConnectedLocationsForm, LocationForm, ImageUploadForm
from .models import *
from django.contrib import messages
# Create your views here.

def index(request):
    return render(request, "core/index.html")

def get_locations(request):
    return render(request, 'core/locations.html', {'locations': Location.nodes.all()})

# class LocationListView(generic.ListView):
#     model = Location
#     paginate_by = 10

#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         context["now"] = timezone.now()
#         return context
    
def new_location(request):
    
    if request.method == 'POST':
        location_form = LocationForm(request.POST)
        connected_locations_form = ConnectedLocationsForm(request.POST)
        image_upload_form = ImageUploadForm(request.POST, request.FILES)
        if location_form.is_valid() and connected_locations_form.is_valid() and image_upload_form.is_valid():
            location = location_form.save()
            distance = connected_locations_form.cleaned_data['distance']
            travel_time = connected_locations_form.cleaned_data['travel_time']
            nearest_location = connected_locations_form.cleaned_data['connected_location_input']
            location.connected_locations.connect(Location.nodes.get(name=nearest_location), {'distance':distance, 'travel_time': travel_time})
            messages.success(request, 'Ажмилттай үүсгэлээ!')
            return redirect('core:index') 
        else:
            print("error form")
    else:
        location_form = LocationForm()
        connected_locations_form = ConnectedLocationsForm()
        image_upload_form = ImageUploadForm()

    return render(request, 'core/new_location.html', {'location_form': location_form, 'connected_locations_form': connected_locations_form})