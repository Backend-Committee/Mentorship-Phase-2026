from django import forms

class CartItemForm(forms.Form):
    quantity = forms.IntegerField(min_value=1)

from django.forms import formset_factory

CartItemFormSet = formset_factory(CartItemForm)

CATEGORY_CHOICES = [('all', 'All')]
def get_choices(self):
    return CATEGORY_CHOICES

class FilterForm(forms.Form):
    search = forms.CharField(required=False)
    category = forms.ChoiceField(required=False)
    available_only = forms.BooleanField(required=False)
    
    def __init__(self, *args, **kwargs):
        choices = kwargs.pop('choices', [])
        super(FilterForm, self).__init__(*args, **kwargs)
        self.fields['category'].choices = choices

class ItemQuantityForm(forms.Form):
    product_id = forms.IntegerField(widget=forms.HiddenInput)
    
    def __init__(self, *args, **kwargs):
        stock = kwargs.pop('stock', None)
        super(ItemQuantityForm, self).__init__(*args, **kwargs)
        self.fields['quantity'] = forms.IntegerField(min_value=1, initial=1, max_value=stock, required=True)

class BaseItemQuantityFormSet(forms.BaseFormSet):
    def get_form_kwargs(self, index):
        kwargs = super().get_form_kwargs(index)
        target = kwargs.get(index)
        if target is not None:
            return target
        return kwargs
        
    
ItemQuantityFormSet = formset_factory(ItemQuantityForm, BaseItemQuantityFormSet, extra=0)