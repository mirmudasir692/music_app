from django.dispatch import Signal, receiver
from django.db.models.signals import post_save, post_delete
from music.models import PlayList,MusicAudio


# @receiver(post_delete,sender=MusicAudio)
# def RemoveSongOnDel(sender,instance,**kwargs):
#     song_instance=instance.song