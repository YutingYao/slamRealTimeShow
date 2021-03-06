# Generated by Django 3.1.2 on 2021-05-06 09:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pointCloud', '0006_auto_20210506_1737'),
    ]

    operations = [
        migrations.CreateModel(
            name='CirclePoint2',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('circle_point_id', models.IntegerField(default=0, verbose_name='回环点id')),
                ('circle_point_start', models.CharField(blank=True, max_length=100, null=True, verbose_name='开始回环点')),
                ('circle_point_end', models.CharField(blank=True, max_length=100, null=True, verbose_name='结束回环点')),
            ],
            options={
                'verbose_name': '回环点',
                'verbose_name_plural': '回环点',
                'db_table': 'tb_circle_point2',
            },
        ),
        migrations.DeleteModel(
            name='CirclePoint',
        ),
    ]
