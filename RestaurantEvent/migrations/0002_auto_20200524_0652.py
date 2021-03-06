# Generated by Django 2.2.4 on 2020-05-24 06:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('RestaurantEvent', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='event',
            name='date',
            field=models.DateField(default="2020-07-13"),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='event',
            name='spots_available',
            field=models.IntegerField(default=25, max_length=1000),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='event',
            name='time',
            field=models.TimeField(default="23:15"),
            preserve_default=False,
        ),
    ]
