# Generated by Django 4.2.4 on 2023-08-29 10:53

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Artist',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
                ('listens', models.BigIntegerField(default=0)),
                ('joined_on', models.DateField(auto_now_add=True)),
                ('songs', models.IntegerField(blank=True, default=0, null=True)),
                ('rating', models.IntegerField(default=0)),
            ],
            options={
                'ordering': ['joined_on'],
            },
        ),
    ]
