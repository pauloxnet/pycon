# Generated by Django 2.2.4 on 2019-08-11 19:53

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('conferences', '0006_conference_maps_link'),
    ]

    operations = [
        migrations.RenameField(
            model_name='conference',
            old_name='maps_link',
            new_name='map_link',
        ),
    ]