# Generated by Django 3.2.8 on 2021-11-08 00:36

from django.db import migrations
import martor.models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0005_alter_newfeed_options'),
    ]

    operations = [
        migrations.AlterField(
            model_name='newfeed',
            name='description',
            field=martor.models.MartorField(max_length=10000),
        ),
    ]
