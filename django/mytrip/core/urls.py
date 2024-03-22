from django.urls import path

from . import views 

app_name = "core"
urlpatterns = [
    path("", views.index, name="index"),
    path("locations/", views.get_locations, name="get_locations"),
    path("new_location/", views.new_location, name="new_location"),
    path("new_location", views.new_location, name="new_location")
]
