# Generated by Django 4.2.3 on 2024-01-25 06:29

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('school', '0012_talentprogram_alter_academicinfo_registration_no_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='academicinfo',
            name='registration_no',
            field=models.IntegerField(default=801944, unique=True),
        ),
        migrations.CreateModel(
            name='CounselingSession',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('chat_room_link', models.CharField(max_length=255, unique=True)),
                ('date', models.DateTimeField()),
                ('student', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='student_sessions', to=settings.AUTH_USER_MODEL)),
                ('teacher', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='teacher_sessions', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
