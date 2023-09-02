from django.contrib import admin
from music.models import MusicAudio, PlayList, history, Watch_Later
# Register your models here.


@admin.register(MusicAudio)
class MusicAduioAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'artist', 'views', 'released_on', 'catagory']


@admin.register(PlayList)
class PlaylistAdmin(admin.ModelAdmin):
    list_display = ['name', 'songs']


admin.site.register(Watch_Later)
admin.site.register(history)
