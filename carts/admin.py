from django.contrib import admin
from .models import Cart, CartItem

class CartAdmin(admin.ModelAdmin):
    list_display = ['cart_id', 'date_added', ' cart__cart_id']

class CartItemAdmin(admin.ModelAdmin):
    list_display = ['product', 'variations', 'quantity', 'time_added']

admin.site.register(Cart)
admin.site.register(CartItem)
