from django.db import models
# Create your models here.
from django_neomodel import DjangoNode
from neomodel import *
from django import forms

class Province(DjangoNode):
    uid = UniqueIdProperty(primary_key=True)
    name_eng = StringProperty()
    name_mn = StringProperty()

    class Meta:
        app_label = "mytrip"
    
    def __str__(self):
        return self.name

# class BookForm(ModelForm):
#     class Meta:
#         model = Book
#         fields = ['title', 'age']
    
class Soum(DjangoNode):
    uid = UniqueIdProperty(primary_key=True)
    name_eng = StringProperty()
    name_mn = StringProperty()
    class Meta:
        app_label = "mytrip"
    
    def __str__(self):
        return self.name
    
    
class ConnectedLocations(StructuredRel):
    distance = FloatProperty()
    travel_time = IntegerProperty()


class Location(DjangoNode):
    uid = UniqueIdProperty(primary_key=True)
    name = StringProperty()
    soum = Relationship('Soum', 'IS_IN')
    type = StringProperty()
    category = ArrayProperty()
    description = StringProperty()
    images = ArrayProperty()
    latitude = FloatProperty()
    longitude = FloatProperty()
    connected_locations = Relationship('Location', 'CONNECTS_TO', model=ConnectedLocations)
    class Meta:
        app_label = "mytrip"
    
    def __str__(self):
        return self.name
