# Generated by Django 4.2.4 on 2023-08-29 17:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('live_interaction', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='room',
            name='state',
            field=models.BooleanField(blank=True, default=False, null=True),
        ),
    ]