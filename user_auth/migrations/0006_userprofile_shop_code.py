# Generated by Django 5.2.1 on 2025-07-05 05:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user_auth', '0005_remove_userprofile_category_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='userprofile',
            name='shop_code',
            field=models.CharField(editable=False, max_length=6, null=True, unique=True, verbose_name='shop code'),
        ),
    ]
