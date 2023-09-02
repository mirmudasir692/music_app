from django.contrib import admin
from artists.models import Artist
# Register your models here.


@admin.register(Artist)
class ArtistAdmin(admin.ModelAdmin):
    list_display = ['name', 'listens', 'songs', 'joined_on']
