# Generated by Django 4.2.3 on 2024-01-30 04:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('school', '0014_alter_academicinfo_registration_no_certificate'),
    ]

    operations = [
        migrations.AlterField(
            model_name='academicinfo',
            name='registration_no',
            field=models.IntegerField(default=616975, unique=True),
        ),
    ]
