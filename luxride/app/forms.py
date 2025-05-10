from django import forms
from .models import Car, BorrowedCar


class CarForm(forms.ModelForm):
    class Meta:
        model = Car
        fields = ['make', 'model', 'year', 'description',
                  'available', 'rental_price', 'image']

    image = forms.ImageField(required=True)


class BorrowedCarForm(forms.ModelForm):
    class Meta:
        model = BorrowedCar
        fields = ['status']
        widgets = {
            'status': forms.Select(attrs={'class': 'border px-2 py-1 rounded text-sm'}),
        }
