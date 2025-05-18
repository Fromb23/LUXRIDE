from django.contrib.auth.forms import PasswordResetForm, SetPasswordForm
from django.contrib.auth import get_user_model
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


User = get_user_model()


class CustomPasswordResetForm(PasswordResetForm):
    def get_users(self, email):
        """Returns all matching users (regardless of is_active)"""
        return User.objects.filter(email__iexact=email)


class CustomSetPasswordForm(SetPasswordForm):
    def __init__(self, user, *args, **kwargs):
        super().__init__(user, *args, **kwargs)

    def save(self, commit=True):
        password = self.cleaned_data["new_password1"]
        self.user.set_password(password)
        if commit:
            self.user.save()
        return self.user
