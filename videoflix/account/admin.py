from django.contrib import admin
from .models import PasswordResetToken, UserProfile



class UserProfileAdmin(admin.ModelAdmin):
    # fields = ('text','created_at', 'author', 'receiver')
    list_display = ('id','user','last_logged_in', 'created_at')
    search_fields = ('text',)


class PasswordResetTokenAdmin(admin.ModelAdmin):
    list_display = ('user', 'reset_password_token')


admin.site.register(UserProfile,UserProfileAdmin)
admin.site.register(PasswordResetToken, PasswordResetTokenAdmin)
