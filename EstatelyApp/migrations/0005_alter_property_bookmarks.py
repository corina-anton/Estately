# Generated by Django 3.2.4 on 2021-11-25 19:06

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('EstatelyApp', '0004_property_bookmarks'),
    ]

    operations = [
        migrations.AlterField(
            model_name='property',
            name='bookmarks',
            field=models.ManyToManyField(related_name='bookmarks', to=settings.AUTH_USER_MODEL),
        ),
    ]
