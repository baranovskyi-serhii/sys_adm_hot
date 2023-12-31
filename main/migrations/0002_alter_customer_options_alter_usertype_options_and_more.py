# Generated by Django 4.2.1 on 2023-06-01 10:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
        ('main', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='customer',
            options={'verbose_name': 'user', 'verbose_name_plural': 'users'},
        ),
        migrations.AlterModelOptions(
            name='usertype',
            options={},
        ),
        migrations.AlterField(
            model_name='customer',
            name='groups',
            field=models.ManyToManyField(blank=True, help_text='The groups this user belongs to.', related_name='customer_set', related_query_name='customer', to='auth.group', verbose_name='groups'),
        ),
        migrations.AlterField(
            model_name='customer',
            name='user_permissions',
            field=models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='customer_set', related_query_name='customer', to='auth.permission', verbose_name='user permissions'),
        ),
    ]
