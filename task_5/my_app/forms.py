from django import forms

class CartItemForm(forms.Form):
    quantity = forms.IntegerField(min_value=1)

from django.forms import formset_factory

CartItemFormSet = formset_factory(CartItemForm)