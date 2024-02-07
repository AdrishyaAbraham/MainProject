# Generated by Django 4.2.3 on 2024-02-05 06:36

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('school', '0028_alter_academicinfo_registration_no'),
    ]

    operations = [
        migrations.AlterField(
            model_name='academicinfo',
            name='registration_no',
            field=models.IntegerField(default=184487, unique=True),
        ),
        migrations.CreateModel(
            name='OnlineExam',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('subject', models.CharField(max_length=50)),
                ('date', models.DateField()),
                ('is_open', models.BooleanField(default=False)),
                ('start_time', models.TimeField()),
                ('end_time', models.TimeField()),
                ('min_age', models.IntegerField()),
                ('max_age', models.IntegerField()),
                ('is_published', models.BooleanField(default=False)),
                ('academic_session', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='school.session')),
                ('class_name', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='school.classinfo')),
                ('teacher', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='school.guideteacher')),
            ],
        ),
    ]