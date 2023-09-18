# Generated by Django 4.2.3 on 2023-09-18 14:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('teacher', '0005_alter_educationinfo_passing_year_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='personalinfo',
            name='address',
            field=models.CharField(max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='personalinfo',
            name='email',
            field=models.CharField(max_length=30, unique=True),
        ),
    ]
