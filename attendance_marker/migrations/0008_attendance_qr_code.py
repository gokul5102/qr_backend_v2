# Generated by Django 4.0.6 on 2022-08-04 06:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('attendance_marker', '0007_student_email'),
    ]

    operations = [
        migrations.AddField(
            model_name='attendance',
            name='qr_code',
            field=models.ImageField(null=True, upload_to='images'),
        ),
    ]