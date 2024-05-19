from django import forms
from core.models import Location, Comment

class LocationForm(forms.ModelForm):
    class Meta:
        model = Location
        exclude = ['uid', 'date_added']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for field_name, field in self.fields.items():
            if(field_name != "category"):
                if(field_name == "type"):
                    field.widget.attrs.update({
                        'class': 'form-select',
                    })
                else:
                    field.widget.attrs.update({
                        'class': 'form-control',
                    })
            
    TYPE_CHOICES = [
        ('Энгийн', 'Энгийн'),
        ('Явган', 'Явган'),
        ('Экстрем', 'Экстрем'),
    ]
    type = forms.ChoiceField(choices=TYPE_CHOICES)

    CATEGORY_CHOICES = [
        ('Түүхэн дурсгалт', 'Түүхэн дурсгалт'),
        ('Уул хад', 'Уул хад'),
        ('Ой мод', 'Ой мод'),
        ('Ус нуур, гол цөөрөм', 'Ус нуур, гол мөрөн'),
        ('Хээр тал', 'Хээр тал'),
        ('Говь цөл', 'Говь цөл'),
        ('Хөшөө дурсгал', 'Хөшөө дурсгал'),
        ('Бусад', 'Бусад'),
    ]
    category = forms.MultipleChoiceField(choices=CATEGORY_CHOICES, widget=forms.CheckboxSelectMultiple)
    image_url = forms.ImageField()
    description = forms.CharField(widget=forms.Textarea)

class ConnectedLocationPropertyForm(forms.Form):
    def __init__(self, *args, **kwargs):
        connected_locations = kwargs.pop('connected_locations', [])
        super(ConnectedLocationPropertyForm, self).__init__(*args, **kwargs)
        for connected_location in connected_locations:
            self.fields[f'connected_location_{connected_location.uid}'] = forms.BooleanField(label=connected_location.name, required=False)

class RequirementForm(forms.Form):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for field_name, field in self.fields.items():
            if(field_name != "category"):
                field.widget.attrs.update({
                    'class': 'form-select',
                })

    TYPE_CHOICES = [
        ('Энгийн', 'Энгийн'),
        ('Явган', 'Явган'),
        ('Экстрем', 'Экстрем'),
    ]
    CATEGORY_CHOICES = [
        ('Түүхэн дурсгалт', 'Түүхэн дурсгалт'),
        ('Уул хад', 'Уул хад'),
        ('Ой мод', 'Ой мод'),
        ('Ус нуур, гол цөөрөм', 'Ус нуур, гол мөрөн'),
        ('Хээр тал', 'Хээр тал'),
        ('Говь цөл', 'Говь цөл'),
        ('Хөшөө дурсгал', 'Хөшөө дурсгал'),
        ('Бусад', 'Бусад'),
    ]
    DURATION_CHOICES = [
        ('1', '1 өдрийн дотор'),
        ('2', '1-2 өдөр'),
        ('3', '2-3 өдөр'),
        ('4', '3-5 өдөр'),
        ('5', '5-с дээш өдөр'),
    ]
    BUDGET_CHOICES = [
        ('1', '100000₮ дотор'),
        ('2', '100000-200000₮'),
        ('3', '200000-300000₮'),
        ('4', '300000-500000₮'),
        ('5', '500000-1000000₮'),
        ('6', '1000000-2000000₮'),
        ('7', '2000000₮-өөс дээш'),
    ]
    CAR_CHOICES = [
        ('1', 'Prius 10'),
        ('1', 'Prius 20'),
        ('1', 'Prius 30'),
        ('1', 'Prius 40'),
        ('2', 'Land Cruiser 80'),
        ('2', 'Land Cruiser 90'),
        ('2', 'Land Cruiser 100/Lexus 470'),
        ('2', 'Land Cruiser 200/Lexus 570'),
        ('2', 'Land Cruiser 300/Lexus 670'),
    ]
    
    type = forms.ChoiceField(choices=TYPE_CHOICES, label="Аяллын төрөл", required=True)
    category = forms.MultipleChoiceField(choices=CATEGORY_CHOICES, widget=forms.CheckboxSelectMultiple, label="Аяллын сэдэв", required=True)
    duration = forms.ChoiceField(choices=DURATION_CHOICES, label="Аяллын хугацаа", required=True)
    budget = forms.ChoiceField(choices=BUDGET_CHOICES, label="Аяллын төсөв", required=True)
    car = forms.ChoiceField(choices=CAR_CHOICES, label="Автомашин", required=True)

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        exclude = ['uid', 'commenter_id', 'location', 'created_at']
    body = forms.CharField(widget=forms.Textarea, label='')
    stars = forms.IntegerField(min_value=0, max_value=5, label='Үнэлгээ')