# Generated by Django 4.2.3 on 2023-09-18 15:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('school', '0034_alter_academicinfo_registration_no'),
    ]

    operations = [
        migrations.AlterField(
            model_name='academicinfo',
            name='registration_no',
            field=models.IntegerField(default=353728, unique=True),
        ),
    ]
