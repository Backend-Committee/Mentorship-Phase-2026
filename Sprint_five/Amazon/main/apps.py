# apps.py

import os
from django.apps import AppConfig

class MainConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'main'

    def ready(self):
        if os.environ.get('RUN_MAIN') == 'true':
            from cart.models import CartItem
            cart_items = CartItem.objects.all()
            for item in cart_items:
                item.delete()