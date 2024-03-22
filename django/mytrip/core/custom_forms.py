from django import forms
from .models import *

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

    # PROVINCE_CHOICES = [
    #     ('Ulaanbaatar', 'Улаанбаатар'),
    #     ('Bayan-Ulgii', 'Баян-Өлгий'),
    #     ('Khovd', 'Ховд'),
    #     ('Uvs', 'Увс'),
    #     ('Zavkhan', 'Завхан'),
    #     ('Gobi-Altai', 'Говь-Алтай'),
    #     ('Arkhangai', 'Архангай'),
    #     ('Uvurkhangai', 'Өвөрхангай'),
    #     ('Khuvsgul', 'Хөвсгөл'),
    #     ('Bulgan', 'Булган'),
    #     ('Umnugovi', 'Өмнөговь'),
    #     ('Dundgovi', 'Дундговь'),
    #     ('Govisumber', 'Говьсүмбэр'),
    #     ('Tuv', 'Төв'),
    #     ('Selenge', 'Сэлэнгэ'),
    #     ('Darkhan-Uul', 'Дархан-Уул'),
    #     ('Orkhon', 'Орхон'),
    #     ('Dornogovi', 'Дорноговь'),
    #     ('Sukhbaatar', 'Сүхбаатар'),
    #     ('Khentii', 'Хэнтий'),
    #     ('Dornod', 'Дорнод'),
    #     ('Bayankhongor', 'Баянхонгор'),
    # ]
    # province = forms.ChoiceField(choices=PROVINCE_CHOICES)

    images = forms.CharField(widget=forms.Textarea)

# class ConnectedLocationsForm(forms.Form):
#     print(Location.nodes.all())