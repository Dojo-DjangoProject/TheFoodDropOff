# Generated by Django 2.2.4 on 2020-05-26 18:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('RestaurantItem', '0002_item_restaurant'),
    ]

    operations = [
        migrations.RenameField(
            model_name='item',
            old_name='price',
            new_name='item_price',
        ),
        migrations.RemoveField(
            model_name='item',
            name='name',
        ),
        migrations.AddField(
            model_name='item',
            name='item_description',
            field=models.TextField(default='desc'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='item',
            name='item_title',
            field=models.CharField(default='item', max_length=255),
            preserve_default=False,
        ),
    ]
