# Generated by Django 4.2.3 on 2023-09-18 14:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('school', '0031_alter_academicinfo_registration_no_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='academicinfo',
            name='registration_no',
            field=models.IntegerField(default=322242, unique=True),
        ),
    ]