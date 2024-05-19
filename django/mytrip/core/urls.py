from django.urls import path
from . import views 

app_name = "core"
urlpatterns = [
    path("", views.index, name="index"),
    path("locations/", views.get_locations, name="locations"),
    path("new_location/", views.new_location, name="new_location"),
    path('soums/', views.soums, name='soums'),
    path('connected_locations_properties/', views.connected_locations_properties, name="connected_locations_properties"),
    path('new_trip/', views.new_trip, name='new_trip'),
    path('locations/<int:pk>/', views.location_detail, name='location_detail'),
]
