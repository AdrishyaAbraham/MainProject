# Generated by Django 4.2.3 on 2023-08-21 07:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('school', '0002_student_delete_user'),
    ]

    operations = [
        migrations.CreateModel(
            name='Teacher',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('teacher_number', models.PositiveBigIntegerField()),
                ('name', models.CharField(max_length=60)),
                ('email', models.EmailField(max_length=100)),
            ],
        ),
    ]