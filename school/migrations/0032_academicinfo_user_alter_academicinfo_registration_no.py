# Generated by Django 4.2.3 on 2024-02-07 06:22

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('school', '0031_examschedule_option_question_studentanswer_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='academicinfo',
            name='user',
            field=models.OneToOneField(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='academic_info', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='academicinfo',
            name='registration_no',
            field=models.IntegerField(default=982044, unique=True),
        ),
    ]
