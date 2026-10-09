from django.contrib import admin
from .models import Product, Variation, VariationManager,WishList, WishListItem

class ProductAdmin(admin.ModelAdmin):
    list_display = ['product_name', 'price', 'stock', 'is_available', 'created_date']
    prepopulated_fields = {'slug': ('product_name',)}

class VariationAdmin(admin.ModelAdmin):
    list_display = ['product','variation_category', 'variation_value', 'is_active', 'created_date', 'time_added']
    list_editable = ['is_active']
    

admin.site.register(Product, ProductAdmin)
admin.site.register(Variation, VariationAdmin)
admin.site.register(WishList)