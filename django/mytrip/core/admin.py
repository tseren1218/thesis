from django.contrib import admin as dj_admin
from django_neomodel import admin as neo_admin
from .custom_forms import *
from .models import *
# Register your models here.

class LocationAdmin(dj_admin.ModelAdmin):
    form = LocationForm

    # def add_view(self, request, form_url='', extra_content=None):
    #     self.inlines = [RelationshipInline]

    list_display = ("name", "soum", "type", "category", "description", "images", "latitude", "longitude", "connected_locations")


neo_admin.register(Location, LocationAdmin)

