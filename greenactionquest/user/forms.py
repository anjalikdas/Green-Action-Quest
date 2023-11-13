
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import CustomUser
from .models import CarbonFootprintData

class CarbonFootprintDataForm(forms.ModelForm):
    class Meta:
        model = CarbonFootprintData
        fields = '__all__'  # Use all fields from the model

class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(required=True)
    first_name = forms.CharField(max_length=30, required=True)
    last_name = forms.CharField(max_length=30, required=True)

    class Meta:
        model = CustomUser
        fields = ['email', 'first_name', 'last_name', 'password']
