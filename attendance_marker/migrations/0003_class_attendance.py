# Generated by Django 4.0.6 on 2022-08-01 10:18

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('attendance_marker', '0002_attendance_present'),
    ]

    operations = [
        migrations.CreateModel(
            name='Class_attendance',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Physics', models.IntegerField(default=0, null=True)),
                ('Chemistry', models.IntegerField(default=0, null=True)),
                ('Maths', models.IntegerField(default=0, null=True)),
                ('student', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='attendance_marker.student')),
            ],
        ),
    ]
