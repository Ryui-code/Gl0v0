from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import *

@admin.register(User)
class UserAdmin(UserAdmin):
    fieldsets = [
        (None, {
            'classes':('wide',),
            'fields': (
                'username', 'password', 'status', 'data_registered', 'token'
            ),
        }),
    ]
    readonly_fields = ['token', 'data_registered']

admin.site.register(Store)
admin.site.register(StoreRating)
admin.site.register(CourierRating)
admin.site.register(Cart)
admin.site.register(Order)