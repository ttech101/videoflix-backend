from django.contrib import admin

from .models import UserProfile



class UserProfileAdmin(admin.ModelAdmin):
    # fields = ('text','created_at', 'author', 'receiver')
    list_display = ('user','last_logged_in', 'created_at')
    search_fields = ('text',)


# Register your models here.

admin.site.register(UserProfile,UserProfileAdmin)
