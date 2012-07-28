from django.db import models

class LibMod(models.Model):
	name = models.CharField(max_length=200)
	description = models.CharField(max_length=200)
	image = models.ImageField(upload_to="libmodimages")
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
	

