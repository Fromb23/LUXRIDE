from django import forms
from .models import Car


class CarForm(forms.ModelForm):
    class Meta:
        model = Car
        fields = ['make', 'model', 'year',
                  'available', 'rental_price', 'image']

    image = forms.ImageField(required=True)
