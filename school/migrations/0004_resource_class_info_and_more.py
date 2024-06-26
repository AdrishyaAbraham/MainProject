# Generated by Django 4.2.3 on 2023-10-11 00:37

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('school', '0003_remove_guardianinfo_student_personalinfo_guardian_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='resource',
            name='class_info',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='school.classinfo'),
        ),
        migrations.AlterField(
            model_name='academicinfo',
            name='registration_no',
            field=models.IntegerField(default=721991, unique=True),
        ),
    ]
