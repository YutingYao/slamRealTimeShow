# Generated by Django 3.1.2 on 2021-05-24 05:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pointCloud', '0011_auto_20210524_1129'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='project',
            options={'verbose_name': '扫描项目', 'verbose_name_plural': '扫描项目'},
        ),
        migrations.AlterField(
            model_name='project',
            name='id',
            field=models.AutoField(primary_key=True, serialize=False, verbose_name='项目编号'),
        ),
    ]
