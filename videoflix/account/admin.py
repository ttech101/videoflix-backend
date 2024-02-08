from django.contrib import admin
from .models import PasswordResetToken, UserProfile



class UserProfileAdmin(admin.ModelAdmin):
    """
    Admin class for the UserProfile model.
    This class defines the display options for the UserProfile model in the Django admin panel.
    Attributes:
        list_display (tuple): The fields to be displayed in the list of user profiles.
        search_fields (tuple): The fields to search for in the Django admin panel.
    """
    list_display = ('id','user','last_logged_in', 'created_at')
    search_fields = ('text',)


class PasswordResetTokenAdmin(admin.ModelAdmin):
    """
    Admin class for the PasswordResetToken model.
    This class defines the display options for the PasswordResetToken model in the Django admin panel.
    Attributes:
        list_display (tuple): The fields to be displayed in the list of password reset tokens.
    """
    list_display = ('user', 'reset_password_token')

admin.site.register(UserProfile,UserProfileAdmin)
admin.site.register(PasswordResetToken, PasswordResetTokenAdmin)
