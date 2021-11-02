# Generated by Django 3.2.4 on 2021-11-02 13:36

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('EstatelyApp', '0002_photo'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='photo',
            name='property_id',
        ),
        migrations.AddField(
            model_name='photo',
            name='property',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='EstatelyApp.property'),
        ),
    ]