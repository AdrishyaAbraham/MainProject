# Generated by Django 4.2.3 on 2023-09-10 17:23

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('school', '0009_rename_resource_pdf_resource_resource_file_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='student',
            name='student_number',
        ),
    ]
