# Generated by Django 4.2.1 on 2023-06-05 16:18

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0022_image_created_at'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Facility',
            new_name='Faciliti',
        ),
        migrations.RenameField(
            model_name='room',
            old_name='facility',
            new_name='conveniences',
        ),
    ]
