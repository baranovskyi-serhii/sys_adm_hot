# Generated by Django 4.2.1 on 2023-06-02 16:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0006_alter_customer_user_type'),
    ]

    operations = [
        migrations.AddField(
            model_name='usertype',
            name='lock_type',
            field=models.BooleanField(blank=True, default=False, null=True),
        ),
    ]