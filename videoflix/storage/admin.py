from django.contrib import admin

from .models import uploadMovie

# Register your models here.

class UploadMovieAdmin(admin.ModelAdmin):
    # fields = ('text','created_at', 'author', 'receiver')
    list_display = ('id','user','last_play', 'created_at','movie_name','author')
    search_fields = ('text',)


admin.site.register(uploadMovie,UploadMovieAdmin)