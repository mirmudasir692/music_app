from django.dispatch import receiver, Signal
from music.models import MusicAudio
from django.db.models.signals import post_save, post_delete
from django.conf import settings
from django.core.mail import send_mail
from Users.models import CustomUser


@receiver(post_save, sender=MusicAudio)
def update_songs_after_music_add(sender, instance, created, **kwargs):
    if created:
        artist = instance.artist
        artist.songs += 1
        artist.save()
        # send_emails_whenSongOut()


def send_emails_whenSongOut():
    subject = 'new song out '
    message = 'hello guys, new blockbustor song is released'
    from_email = 'mirmudasir692@yahoo.com'
    users = CustomUser.objects.all()
    for user in users:
        recipient_list = [user.email]
        send_mail(subject, message, from_email, recipient_list)


@receiver(post_delete, sender=MusicAudio)
def decrease_songs_after_delete(sender, instance, **kwargs):
    artist = instance.artist
    artist.songs -= 1
    artist.save()
    storage, path = instance.audio.storage, instance.audio.path
    if storage.exists(path):
        storage.delete(path)
    storage, path = instance.image.storage, instance.image.path
    if storage.exists(path):
        storage.delete(path)
