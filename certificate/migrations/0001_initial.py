# Generated by Django 4.2.3 on 2024-02-28 04:51

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Certificate_url',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('certificate_id', models.CharField(max_length=1000)),
            ],
        ),
        migrations.CreateModel(
            name='Event',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('event_name', models.CharField(max_length=250)),
                ('event_type', models.CharField(max_length=250)),
                ('starting_date', models.DateField()),
                ('ending_date', models.DateField(null=True)),
                ('csv_file', models.FileField(upload_to='certificates/csv_files/')),
                ('template', models.FileField(upload_to='certificates/templates/')),
                ('name_column', models.CharField(blank=True, max_length=250, null=True)),
                ('email_column', models.CharField(blank=True, max_length=250, null=True)),
                ('org_column', models.CharField(blank=True, max_length=250, null=True)),
                ('message', models.TextField(blank=True, null=True)),
                ('slug', models.SlugField(blank=True, null=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Participant',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=250)),
                ('email', models.CharField(max_length=250)),
                ('org', models.CharField(max_length=250)),
                ('status', models.BooleanField(default=False)),
                ('event', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='certificate.event')),
            ],
        ),
    ]
