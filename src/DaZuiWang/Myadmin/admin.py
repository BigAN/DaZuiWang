from django.contrib.auth.admin import UserAdmin
from django.contrib import admin
from django.contrib.auth.models import User
from Myadmin.models import UserProfile
class ProfileInline(admin.StackedInline):
    model=UserProfile
    max_num=1
    can_delete=False
    
class CustomUserAdmin(UserAdmin):
    inlines= [ProfileInline,]

admin.site.unregister(User)
admin.site.register(User, CustomUserAdmin)