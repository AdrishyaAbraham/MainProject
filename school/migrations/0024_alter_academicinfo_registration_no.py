# Generated by Django 4.2.3 on 2024-02-05 04:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('school', '0023_alter_academicinfo_registration_no'),
    ]

    operations = [
        migrations.AlterField(
            model_name='academicinfo',
            name='registration_no',
            field=models.IntegerField(default=239291, unique=True),
        ),
    ]
