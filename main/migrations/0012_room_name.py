# Generated by Django 4.2.1 on 2023-06-05 07:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0011_image_room_images'),
    ]

    operations = [
        migrations.AddField(
            model_name='room',
            name='name',
            field=models.CharField(blank=True, max_length=500, null=True),
        ),
    ]
