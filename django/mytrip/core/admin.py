from django.contrib import admin as dj_admin
from .models import *
from django_neomodel import admin as neo_admin
from django import forms
# Register your models here.

class LocationForm(ModelForm):
    class Meta:
        model = Location
        fields = '__all__'

    TYPE_CHOICES = [
        ('ordinary', 'Энгийн'),
        ('trek', 'Явган'),
        ('extreme', 'Экстрем'),
    ]
    type = forms.ChoiceField(choices=TYPE_CHOICES)

    CATEGORY_CHOICES = [
        ('historic', 'Түүхэн дурсгалт'),
        ('mountain_and_rocks', 'Уул хад'),
        ('forest', 'Ой мод'),
        ('water', 'Ус нуур, гол мөрөн'),
        ('plain', 'Хээр тал'),
        ('desert', 'Говь цөл'),
        ('monument', 'Хөшөө дурсгал'),
        ('other', 'Бусад'),
    ]
    category = forms.ChoiceField(choices=CATEGORY_CHOICES)

    images = forms.CharField(widget=forms.Textarea)
  
class LocationAdmin(dj_admin.ModelAdmin):
    form = LocationForm
    list_display = ("name", "soum", "type", "category", "description", "images", "latitude", "longitude", "nearest_location")

neo_admin.register(Location, LocationAdmin)