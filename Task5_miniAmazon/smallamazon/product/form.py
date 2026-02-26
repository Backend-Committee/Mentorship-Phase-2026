from django import forms
from .models import product

class AddPro(forms.ModelForm):
    class Meta:
        model = product
        fields = ['name', 'price', 'category', 'image', 'Is_Available', 'stock']