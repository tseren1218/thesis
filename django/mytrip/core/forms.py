from django import forms

from core.models import Location


class LocationForm(forms.ModelForm):
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
    images = forms.FileField()
    description = forms.CharField(widget=forms.Textarea)
    
class ConnectedLocationsForm(forms.Form):
    connected_locations = Location.nodes.all()
    CONNECTED_LOCATION_CHOICES = []
    for connected_location in connected_locations:
        CONNECTED_LOCATION_CHOICES.append((connected_location, connected_location))
    connected_location_input = forms.ChoiceField(choices=CONNECTED_LOCATION_CHOICES)
    distance = forms.FloatField()
    travel_time = forms.FloatField()
