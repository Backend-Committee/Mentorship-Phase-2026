from django import forms
from django.core.exceptions import ValidationError
from .models import Product,Category,CartItem

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = '__all__'
        labels = {
            'name': 'Product Name',
            'price': 'Price',
            'stock': 'Stock',
            'is_Available': 'Is Available'
        }
class AddCategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = '__all__'

class AddToCartForm(forms.ModelForm):
    """Form for adding products to cart with quantity validation"""

    class Meta:
        model = CartItem
        fields = ['quantity']
        widgets = {
            'quantity': forms.NumberInput(attrs={'class': 'form-control', 'min': '1', 'value': '1'}),
        }

    def __init__(self, *args, **kwargs):
        self.product = kwargs.pop('product', None)
        super().__init__(*args, **kwargs)

    def clean_quantity(self):
        """Validate quantity doesn't exceed stock"""
        quantity = self.cleaned_data.get('quantity')

        if quantity is not None and quantity < 1:
            raise ValidationError('Quantity must be at least 1')

        if self.product:
            if quantity > self.product.stock:
                raise ValidationError(f'Only {self.product.stock} items available in stock')

            if not self.product.is_available:
                raise ValidationError('This product is not available')

        return quantity
