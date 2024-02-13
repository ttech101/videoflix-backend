from django.contrib import admin

from .models import uploadMovie

# Register your models here.

class UploadMovieAdmin(admin.ModelAdmin):
    """
    Admin class for the uploadMovie model.
    This class defines the display options for the uploadMovie model in the Django admin panel.
    """
    list_display = ('id','user','last_play', 'created_at','movie_name','author','random_key')
    search_fields = ('text',)


admin.site.register(uploadMovie,UploadMovieAdmin)