# Generated by Django 4.2.4 on 2023-08-29 10:53

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('music', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Room',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
                ('user_num', models.IntegerField(blank=True, default=0, null=True)),
                ('timeFix', models.FloatField(blank=True, default=0.0, null=True)),
                ('admin', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('music', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='music.musicaudio')),
                ('users', models.ManyToManyField(blank=True, related_name='joined_users', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
