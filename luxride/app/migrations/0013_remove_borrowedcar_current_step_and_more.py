# Generated by Django 5.2 on 2025-04-19 15:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0012_car_description_alter_car_image'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='borrowedcar',
            name='current_step',
        ),
        migrations.AddField(
            model_name='customuser',
            name='current_step',
            field=models.PositiveIntegerField(default=1),
        ),
    ]
