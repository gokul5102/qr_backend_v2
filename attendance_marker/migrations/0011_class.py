# Generated by Django 4.0.6 on 2022-08-09 16:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('attendance_marker', '0010_alter_attendance_class_location_x_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='Class',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('room_no', models.IntegerField(default=0)),
                ('lat_1', models.IntegerField(default=0)),
                ('lat_2', models.IntegerField(default=0)),
                ('long_1', models.IntegerField(default=0)),
                ('long_2', models.IntegerField(default=0)),
            ],
        ),
    ]
