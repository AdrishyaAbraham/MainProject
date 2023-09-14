# Generated by Django 4.2.3 on 2023-08-10 04:12

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('email', models.EmailField(max_length=254, unique=True)),
                ('full_name', models.CharField(max_length=255)),
                ('phone_number', models.CharField(max_length=20)),
                ('user_id', models.AutoField(primary_key=True, serialize=False)),
            ],
        ),
    ]
