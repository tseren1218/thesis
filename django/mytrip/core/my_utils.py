from .models import *
import boto3
from django.conf import settings
from neomodel import db
from .templatetags import my_tags
from django.core.paginator import Paginator

class MyUtils:

    # Argumenteeree zuvhun single raw location huleen avna!
    def dereference_location_from_raw(raw_location):
        location = Location.nodes.get_or_none(custom_id=raw_location['custom_id'])
        return location
    
    # Argumenteeree zuvhun single raw relationship avna!
    def dereference_relationship_from_raw(raw_relationship):
        distance = float(raw_relationship['distance'])
        travel_time = int(raw_relationship['travel_time'])
        relationship = LocationRelationship(distance=distance, travel_time=travel_time)
        return relationship

    # Aylliin location-ii zurag huleen avch s3-d upload hiine
    def upload_location_image_to_s3(file):
        s3 = boto3.client('s3', aws_access_key_id=settings.AWS_ACCESS_KEY_ID, aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY)
        bucket_name = settings.AWS_STORAGE_BUCKET_NAME
        key = 'your-folder/' + file.name 
        s3.upload_fileobj(file, bucket_name, key)
        return key

    def paginate(data, page_size, page_number):
        paginator = Paginator(data, page_size)
        return paginator.get_page(page_number)

    def query_trip(request, nth_query):
        trip_type = request.POST.get('type')
        categories = request.POST.getlist('category_checkbox')
        duration = request.POST.get('duration')
        budget = int(request.POST.get('budget'))
        vehicle = request.POST.get('vehicle')
        fuel_consumption = my_tags.calculate_fuel_consumption(vehicle=vehicle)
        gas_price = 2390
        start_point = "Улаанбаатар (0 цэг)"
        

        if (trip_type and categories and duration and budget and vehicle):
            
            nth_query = int(nth_query) * 5
            # Undsen query
            cypher_query = """MATCH path = (n:Location{name:"Улаанбаатар (0 цэг)"})-[:CONNECTS_TO*1..3]-(m:Location) 
                              WITH 
                              reduce(totalDistance = 0, rel in relationships(path) | totalDistance + rel.distance) AS totalDistance,
                              path,reduce(totalTicketPrice = 0, node in nodes(path) | totalTicketPrice + node.price) AS pathTotalTicketPrice,
                              reduce(totalDistance = 0, rel in relationships(path) | totalDistance + rel.distance) / 100 * $fuel_consumption * $gas_price * 2 AS pathTotalGasPrice,
                              [node in nodes(path) WHERE node.type = $trip_type | node] AS trip_type, 
                              """ 
            
            # Category tus buriig oruulah
            for index, category in enumerate(categories):
                # Hamgiin suuliin category bish bol taslaltai bichigdene
                if index != len(categories)-1:
                    print(f"category{index}: ", category, "\n")
                    cypher_query += f"[node in nodes(path) WHERE '{category}' IN node.category | node] AS trip_category{index},"
                else:
                    print(f"category{index}: ", category, "\n")
                    cypher_query += f"[node in nodes(path) WHERE '{category}' IN node.category | node] AS trip_category{index}"
            
            # budget bolon type-aar filterdeh
            cypher_query += """
                              WHERE pathTotalTicketPrice + pathTotalGasPrice <= $budget
                              AND size(trip_type) >= 1 
                            """
            # Category tus bur dor hayj 1 baih filter oruulah
            for index, category in enumerate(categories):
                cypher_query += f" AND size(trip_category{index}) >= 1"
                              
            # Ehleh tseg tugsgul tseg hoorondoo adil bus
            cypher_query += """
                              AND id(n) <> id(m) 
                              RETURN DISTINCT nodes(path),relationships(path), pathTotalTicketPrice + pathTotalGasPrice AS total_cost, totalDistance
                              SKIP $skip
                              LIMIT 5
                            """            

            # Query parameters
            parameters = {
                "start_point": start_point,
                "trip_type": trip_type,
                "fuel_consumption": fuel_consumption,
                "gas_price": gas_price,
                "budget": budget,
                "skip": nth_query
            }

            print(cypher_query)

            # DB-g querydeh
            results = db.cypher_query(cypher_query, params=parameters)

            return results


class LocationRelationship:
    def __init__(self, distance, travel_time):
        self.distance = distance
        self.travel_time = travel_time
    
