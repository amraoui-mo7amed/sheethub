# Generated by Django 5.2.1 on 2025-07-05 04:53

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('user_auth', '0004_userprofile_category_userprofile_phone_number_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='userprofile',
            name='category',
        ),
        migrations.RemoveField(
            model_name='userprofile',
            name='phone_number',
        ),
        migrations.RemoveField(
            model_name='userprofile',
            name='province',
        ),
    ]
