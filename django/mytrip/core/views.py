from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse_lazy
from core.forms import *
from .models import *
from django.conf import settings
from .my_utils import *
from itertools import zip_longest

def index(request):
    return render(request, "core/index.html")

def new_trip(request):

    if request.method == 'POST':

        results = MyUtils.query_trip(request)
        print("Query results: ", results)

        # Tohiroh aylal oldoogui bol results:False damjuulna
        if not results[0]:
            return render(request, 'core/partials/recommendation_results.html', {'alert_message': 'Уучлаарай, тохирох аяллын маршрут олдсонгүй!'})
        
        trips = results[0]

        # Template ruu shideh buh aylluudiin datag aguulah list-uud 
        all_locations = []
        all_relationships = []
        all_costs = []
        all_distances = []

        for trip in trips:
            # Extract trip data
            locations = [Location.inflate(raw_location) for raw_location in trip[0]]
            relationships = [MyUtils.dereference_relationship_from_raw(raw_relationship=raw_relationship) for raw_relationship in trip[1]]
            # Append to lists
            all_locations.append(locations)
            all_relationships.append(relationships)
            all_costs.append(trip[2])
            all_distances.append(trip[3])
            print("ITERATION COMPLETE")

        # pagination
        # current_page = request.POST.get('page', 1)
        # print(current_page)
        # paginated_locations = MyUtils.paginate(all_locations, 4, current_page)
        # paginated_relationships = MyUtils.paginate(all_relationships, 4, current_page)
        
        trips_data = zip_longest(all_locations, all_relationships)
        print('ZIPPING COMPLETE')

        return render(request, 'core/partials/recommendation_results.html', {'trips_data': trips_data, 'all_costs':all_costs, 'all_distances':all_distances, 'vehicle': request.POST.get('vehicle')})
    else:
        return render(request, 'core/new_trip.html', {'alert_message': 'Та аяллын шалгуураа оруулна уу'})

def get_locations(request):
    locations = Location.nodes.all()
    current_page = request.GET.get('page', 1)
    page_data = MyUtils.paginate(locations, 6, current_page)
    return render(request, 'core/locations.html', {'locations': page_data})

def new_location(request):
    if request.method == 'POST':

        location_form = LocationForm(request.POST, request.FILES)

        if location_form.is_valid():

            # zurag hadgalah
            image_key = MyUtils.upload_location_image_to_s3(request.FILES['image_url'])

            # erunhii data hadgalah
            location = location_form.save(commit=False)
            location.image_url = f"https://{settings.AWS_STORAGE_BUCKET_NAME}.s3.amazonaws.com/{image_key}"
            location.name=location_form.cleaned_data['name']
            location.type=location_form.cleaned_data['type']
            location.category=location_form.cleaned_data['category']
            location.description=location_form.cleaned_data['description']
            location.latitude=location_form.cleaned_data['latitude']
            location.longitude=location_form.cleaned_data['longitude']
            location.save()

            # sum, location hoorond ni holboh
            parent_soum = Soum.nodes.get(uid=request.POST.get('soum'))
            parent_soum.locations.connect(location)
            location.soum.connect(parent_soum)

            # location hoorondiin holbolt
            submitted_data = request.POST
            for key, value in submitted_data.items():
                if "distance" in key:
                    connected_location_uid = key.split("/")[1]
                    connected_location = Location.nodes.get(uid=connected_location_uid)
                    distance = float(request.POST.get(f"distance/{connected_location_uid}"))
                    location.connected_locations.connect(connected_location, {'distance': distance})
                    connected_location.connected_locations.connect(location, {'distance': distance})
                    
                if "travel_time" in key:
                    connected_location_uid = key.split("/")[1]
                    connected_location = Location.nodes.get(uid=connected_location_uid)
                    travel_time = int(request.POST.get(f"travel_time/{connected_location_uid}"))
                    relationship_to = location.connected_locations.relationship(connected_location)
                    if relationship_to:
                        relationship_to.travel_time = travel_time
                        relationship_to.save()
                    relationship_from = connected_location.connected_locations.relationship(location)
                    if relationship_from:
                        relationship_from.travel_time = travel_time
                        relationship_from.save()
            return HttpResponseRedirect(reverse_lazy('core:index'))
        else:
            print(location_form.errors)
            return HttpResponse(400)
    else:
        location_form = LocationForm()
        connected_location_candidates = []
        locations = Location.nodes.all()
        for location in locations:
            connected_location_candidates.append(location)
        provinces = Province.nodes.order_by('name')
    return render(request, 'core/new_location.html', {'location_form': location_form, 'provinces': provinces, 'connected_location_candidates': connected_location_candidates})

def soums(request):
    request_province_uid = request.GET.get('province')
    parent_province = Province.nodes.get(uid=request_province_uid)
    soums = parent_province.soums.order_by('name')
    return render(request, 'core/partials/soums.html', {'soums': soums}) 
    
def connected_locations_properties(request):
    connected_location_uids = request.POST.getlist('checkbox_option')
    print(connected_location_uids)
    connected_locations = []
    for connected_location_uid in connected_location_uids:
        connected_location = Location.nodes.get(uid=connected_location_uid)
        connected_locations.append(connected_location)
    return render(request, 'core/partials/connected_locations_properties.html', {'connected_locations': connected_locations})


