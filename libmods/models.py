from django.db import models
from django.utils import encoding

from easy_thumbnails.signals import saved_file
from easy_thumbnails.signal_handlers import generate_aliases_global

saved_file.connect(generate_aliases_global)

class LibMod(models.Model):
	name = models.CharField(max_length=200)
	description = models.CharField(max_length=200)
	image = models.ImageField(upload_to="libmodimages", null=True, blank=True)
	revision = models.IntegerField()
	date_added = models.DateTimeField("date added") 
	ki_version = models.CommaSeparatedIntegerField(max_length=20)
	ki_text = models.TextField()
	part_of_ki = models.BooleanField()
	votes = models.IntegerField()
	class Meta:
		abstract = True
	def __unicode__(self):
		return self.name

class Footprint(LibMod):
	pass

class Component(LibMod):
	footprints = models.ManyToManyField(Footprint, null=True, blank=True)
	

