from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Store, Menu, Review, CustomUser

# Register your models here.
admin.site.register(Store)
admin.site.register(Menu)
admin.site.register(Review)
admin.site.register(CustomUser, UserAdmin)
