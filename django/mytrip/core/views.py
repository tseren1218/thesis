from django.http import HttpResponse, HttpResponseRedirect, StreamingHttpResponse
from django.shortcuts import render
from django.urls import reverse_lazy
from core.forms import *
from .models import *
from django.conf import settings
from neomodel import db
from .my_utils import *
from itertools import zip_longest
from .templatetags import my_tags

def index(request):
    return render(request, "core/index.html")

def new_trip(request):

    if request.method == 'POST':

        trip_type = request.POST.get('type')
        categories = request.POST.getlist('category_checkbox')
        duration = request.POST.get('duration')
        budget = int(request.POST.get('budget'))
        vehicle = request.POST.get('vehicle')
        fuel_consumption = my_tags.calculate_fuel_consumption(vehicle=vehicle)
        gas_price = 2390
        start_point = "Улаанбаатар (0 цэг)"

        if (trip_type and categories and duration and budget and vehicle):
            
            # Undsen query
            cypher_query = """MATCH path = (n:Location{name:"Улаанбаатар (0 цэг)"})-[:CONNECTS_TO*1..3]-(m:Location) 
                              WITH path,reduce(totalTicketPrice = 0, node in nodes(path) | totalTicketPrice + node.price) AS pathTotalTicketPrice, 
                              reduce(totalDistance = 0, rel in relationships(path) | totalDistance + rel.distance) / 100 * $fuel_consumption * $gas_price * 2 AS pathTotalGasPrice,
                              [node in nodes(path) WHERE node.type = $trip_type | node] AS trip_type, 
                              """ 
            
            for index, category in enumerate(categories):
                # Hamgiin suuliin category bish bol taslaltai bichigdene
                if index != len(categories)-1:
                    print(f"category{index}: ", category, "\n")
                    cypher_query += f"[node in nodes(path) WHERE '{category}' IN node.category | node] AS trip_category{index},"
                else:
                    print(f"category{index}: ", category, "\n")
                    cypher_query += f"[node in nodes(path) WHERE '{category}' IN node.category | node] AS trip_category{index}"
            
            cypher_query += """
                              WHERE pathTotalTicketPrice + pathTotalGasPrice <= $budget
                              AND size(trip_type) >= 1 
                            """
            
            for index, category in enumerate(categories):
                cypher_query += f" AND size(trip_category{index}) >= 1"
                              
                              
            cypher_query += """
                              AND id(n) <> id(m) 
                              RETURN nodes(path),relationships(path), pathTotalTicketPrice + pathTotalGasPrice AS total_cost
                            """            

            # Query parameters
            parameters = {
                "start_point": start_point,
                "trip_type": trip_type,
                "fuel_consumption": fuel_consumption,
                "gas_price": gas_price,
                "budget": budget,
            }

            print(cypher_query)

            # DB-g querydeh
            results = db.cypher_query(cypher_query, params=parameters)

            # Tohiroh aylal oldoogui bol results:False damjuulna
            if not results[0]:
                return render(request, 'core/partials/recommendation_results.html', {'alert_message': 'Уучлаарай, тохирох аяллын маршрут олдсонгүй!'})
            
            trips = results[0]

            # Template ruu shideh buh aylluudiin datag aguulah list-uud 
            all_locations = []
            all_relationships = []
            all_prices = []

            print
            for trip in trips:
                # Extract trip data
                locations = [MyUtils.dereference_location_from_raw(raw_location=raw_location) for raw_location in trip[0]]
                relationships = [MyUtils.dereference_relationship_from_raw(raw_relationship=raw_relationship) for raw_relationship in trip[1]]
                price = int(trip[2])

                # Append to lists
                all_locations.append(locations)
                all_relationships.append(relationships)
                all_prices.append([price])

                print("ONE ITERATION COMPLETE")

            trips_data = zip_longest(all_locations, all_relationships)
            
            return render(request, 'core/partials/recommendation_results.html', {'trips_data': trips_data, 'all_prices': all_prices, 'vehicle': vehicle})
    else:
        return render(request, 'core/new_trip.html', {'alert_message': 'Та аяллын шалгуураа оруулна уу'})

def get_locations(request):
    locations = Location.nodes.exclude(name="Улаанбаатар (0 цэг)")
    return render(request, 'core/locations.html', {'locations': locations})

def new_location(request):
    if request.method == 'POST':

        location_form = LocationForm(request.POST, request.FILES)

        if location_form.is_valid():

            # zurag hadgalah
            image_key = MyUtils.upload_location_image_to_s3(request.FILES['image_url'])
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


