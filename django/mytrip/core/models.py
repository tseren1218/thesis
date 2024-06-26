from django_neomodel import DjangoNode
from neomodel import *

class Province(DjangoNode):
    uid = UniqueIdProperty(primary_key=True)
    name = StringProperty()
    soums = RelationshipTo('Soum', 'HAS')
    class Meta:
        app_label = "mytrip"
    def __str__(self):
        return self.name

class Soum(DjangoNode):
    uid = UniqueIdProperty(primary_key=True)
    name = StringProperty()
    province = RelationshipTo('Province', 'IS_IN')
    locations = RelationshipTo('Location', 'HAS')
    class Meta:
        app_label = "mytrip" 
    def __str__(self):
        return self.name
    
class ConnectedLocations(StructuredRel):
    distance = FloatProperty()
    travel_time = IntegerProperty()

class Location(DjangoNode):
    custom_id = IntegerProperty(primary_key=True)
    uid = UniqueIdProperty()
    name = StringProperty()
    soum = RelationshipTo('Soum', 'IS_IN')
    type = StringProperty()
    category = ArrayProperty()
    price = FloatProperty(required=False)
    description = StringProperty()
    image_url = StringProperty()
    latitude = FloatProperty()
    longitude = FloatProperty()
    date_added = DateTimeProperty(default_now=True)
    connected_locations = Relationship('Location', 'CONNECTS_TO', model=ConnectedLocations)
    comments = RelationshipTo('Comment', 'HAS')
    class Meta:
        app_label = "mytrip"
    def __str__(self):
        return self.name

class Comment(DjangoNode):
    uid = UniqueIdProperty(primary_key=True)
    location = RelationshipTo('Location', 'BELONGS_TO')
    commenter_id = IntegerProperty(default=0)
    body = StringProperty(required=True)
    stars = IntegerProperty(required=True, max=5, min=0)
    created_at = DateTimeProperty()
    class Meta:
        app_label = "mytrip" 
    def __str__(self):
        return self.body