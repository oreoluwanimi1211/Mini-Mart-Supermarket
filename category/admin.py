from django.contrib import admin
from .models import Category

class CategoryAdmin(admin.ModelAdmin):
    list_display = ['category_name']
    prepopulated_fields = {'slug': ('category_name',)}
    search_fields = ['category_name', 'description']

admin.site.register(Category, CategoryAdmin)

