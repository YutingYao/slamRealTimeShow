# Generated by Django 3.1.2 on 2021-06-08 05:38

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('pointCloud', '0018_merge_20210608_1338'),
    ]

    operations = [
        migrations.DeleteModel(
            name='BookInfo',
        ),
        migrations.DeleteModel(
            name='Project',
        ),
    ]