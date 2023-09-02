from django.db import models
from artists.models import Artist
from Users.models import CustomUser

# Create your models here.


class MusicAudio(models.Model):
    artist = models.ForeignKey(Artist, on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    released_on = models.DateField(auto_now_add=True)
    views = models.BigIntegerField(default=0)
    image = models.ImageField(default='', upload_to='images/')
    audio = models.FileField(upload_to='music/', default='')
    catagory = models.CharField(max_length=100)
    viewer = models.ManyToManyField(
        CustomUser, related_name='viewed_audios', blank=True)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name


class PlayList(models.Model):
    name = models.CharField(max_length=300, null=True)
    songs = models.BigIntegerField(default=0, null=True)
    music_tracks = models.ManyToManyField(MusicAudio, related_name='playlists')

    def update_songs_count(self):
        self.songs = self.music_tracks.count()

    def add_music_track(self, track):
        self.music_tracks.add(track)
        self.update_songs_count()

    def remove_music_track(self, track):
        self.update_songs_count()

    def __str__(self):
        return self.name


class Watch_Later(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    later_audios = models.ManyToManyField(
        MusicAudio, related_name="watch_later_audios", blank=True)


class history(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    music = models.ManyToManyField(MusicAudio, blank=True)
