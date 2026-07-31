from django.contrib import admin
from .models import CustomUser, UserProfile


class UserAdmin(admin.ModelAdmin):
    list_display = ('email', 'username', 'phone_number', 'is_active')

class UserprofileAdmin(admin.ModelAdmin):
    list_display = ('user__username', 'address','user__email', 'user__phone_number')

admin.site.register(CustomUser, UserAdmin)
admin.site.register(UserProfile, UserprofileAdmin)
