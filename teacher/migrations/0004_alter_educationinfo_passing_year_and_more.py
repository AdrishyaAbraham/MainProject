# Generated by Django 4.2.3 on 2023-09-18 14:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('teacher', '0003_remove_personalinfo_marital_status_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='educationinfo',
            name='passing_year',
            field=models.DateField(),
        ),
        migrations.AlterField(
            model_name='traininginfo',
            name='year',
            field=models.DateField(),
        ),
    ]
