# Generated by Django 4.2.3 on 2024-02-05 04:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('school', '0021_alter_academicinfo_registration_no'),
    ]

    operations = [
        migrations.AlterField(
            model_name='academicinfo',
            name='registration_no',
            field=models.IntegerField(default=439304, unique=True),
        ),
    ]
