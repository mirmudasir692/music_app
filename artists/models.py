from django.db import models

# Create your models here.


class Artist(models.Model):
    name = models.CharField(max_length=200)
    listens = models.BigIntegerField(default=0)
    joined_on = models.DateField(auto_now_add=True)
    songs = models.IntegerField(default=0,null=True,blank=True)
    rating=models.IntegerField(default=0)

    class Meta:
        ordering = ['joined_on', ]

    def __str__(self):
        return self.name
