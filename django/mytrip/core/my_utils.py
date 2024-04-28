from .models import *
import boto3
from django.conf import settings
from neomodel import db

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


    def paginate_nodes(page_number, page_size):
        skip = (page_number - 1) * page_size
        cypher_query = "MATCH (n:Location) RETURN n SKIP $skip LIMIT $limit"
        parameters = {
            "skip": skip,
            "limit": 6,
        }
        results = db.cypher_query(cypher_query, params=parameters)
        return results[0]

class LocationRelationship:
    def __init__(self, distance, travel_time):
        self.distance = distance
        self.travel_time = travel_time
    
