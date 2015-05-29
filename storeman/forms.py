from django import forms
from .models import Item, Location

class ItemCreationForm(forms.ModelForm):
    class Meta:
        model = Item
        exclude = ['slug']
        fields = '__all__'

class LocationCreationForm(forms.ModelForm):
    class Meta:
        model = Location
        exclude = ['slug']
        fields = '__all__'