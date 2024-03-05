from django.db import models

from school.models import *
from django.utils.text import slugify


class Certificate_url(models.Model):
    certificate_id = models.CharField(max_length=1000)


class Event(models.Model):
	user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
	event_name = models.CharField(max_length=250)
	date = models.DateField(auto_now_add=True,null=True)
	csv_file = models.FileField(upload_to="certificates/csv_files/")
	template = models.FileField(upload_to="certificates/templates/")
	email_column = models.CharField(max_length=250, null=True, blank=True)
	subject = models.CharField(max_length=250, null=True)
	message = models.TextField(null=True, blank=True)
	slug = models.SlugField(null=True, blank=True)

	def save(self, *args, **kwargs):
		self.slug = slugify(self.event_name)
		super(Event, self).save(*args, **kwargs)

class Participant(models.Model):
	event = models.ForeignKey(Event, on_delete=models.CASCADE)
	email = models.CharField(max_length=250)
	status = models.BooleanField(default=False)