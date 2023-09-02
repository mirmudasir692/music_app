from django.db import models
from Users.models import CustomUser
from music.models import MusicAudio
# Create your models here.


class Room(models.Model):
    name = models.CharField(max_length=200)
    admin = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    music = models.ForeignKey(MusicAudio, on_delete=models.CASCADE)
    user_num = models.IntegerField(default=0, null=True, blank=True)
    users = models.ManyToManyField(
        CustomUser, blank=True, related_name="joined_users")
    timeFix  = models.FloatField(default=0.0, null=True, blank=True)
    state=models.BooleanField(default=False,null=True,blank=True)

    def __str__(self):
        return self.name
