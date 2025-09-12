from django.contrib import admin

# Register your models here.

from .models import Product  # Ye line Product model ko import karti hai

# Register your models here.
admin.site.register(Product) # Ye line Product model ko admin mein register karti hai