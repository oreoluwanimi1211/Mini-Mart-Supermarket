from django.contrib import admin
from .models import Order, OrderProduct
# Register your models here.

class OrderAdmin(admin.ModelAdmin):
    list_editable = ('first_name','last_name', 'phone_number',
                   'email', 'address_line_1', 'address_line_2',
                     'note', 'city', 'state', 'country'
    )

admin.site.register(Order)
admin.site.register(OrderProduct)