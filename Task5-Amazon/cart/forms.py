from django import forms
# from products.models import Product

class AddToCartForm(forms.Form):
    quantity = forms.IntegerField(min_value=1)

    def __init__(self, *args, product=None, **kwargs):
        super().__init__(*args, **kwargs)
        self.product = product

    def clean_quantity(self):
        quantity = self.cleaned_data['quantity']
        if self.product and quantity > self.product.stock:
            raise forms.ValidationError(
                f"Only {self.product.stock} items available in stock."
            )
        return quantity