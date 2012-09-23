from django.db import models
from django.utils import encoding
from django.contrib.auth.models import User

from easy_thumbnails.signals import saved_file
from easy_thumbnails.signal_handlers import generate_aliases_global
saved_file.connect(generate_aliases_global)

from custom_comments.models import CommentWithFlag
from django.contrib.contenttypes import generic

class LibMod(models.Model):
	''' This is the abstract base model for all library types '''

	name = models.CharField(max_length=200)
	description = models.CharField(max_length=200)
	image = models.ImageField(upload_to="libmodimages", null=True, blank=True)
	revision = models.IntegerField()
	date_added = models.DateTimeField("date added") 
	#the CommaSeparatedIntegerField may not be a good match for this data
	ki_version = models.CommaSeparatedIntegerField(max_length=20)
	ki_text = models.TextField()
	part_of_ki = models.BooleanField()
	votes = models.IntegerField()
	#We associate the comments with the object when they report a problem. 
	#It is a generic relationship as it is a one-to-many relationship which
	#is stored in this model rather than the comments.
	problems_reported = generic.GenericRelation(CommentWithFlag, 
	                                            content_type_field="problem_object_type", 
																							object_id_field="problem_object_id")

	#just a convenience function used during development to print all fields
	def get_fields(self):
		return [(field.name, field.value_to_string(self)) for field in self._meta.fields]

	class Meta:
		abstract = True
	def __unicode__(self):
		return self.name

class Footprint(LibMod):
	#The submitter and maintainer have different related names for different types
	#of libraries so that we can keep the associated libaries seperate when 
	#we look at the maintainer.
	submitter = models.ForeignKey(User, related_name="fp_submitter")
	maintainer = models.ForeignKey(User, related_name="fp_maintainer")

class Component(LibMod):
	submitter = models.ForeignKey(User, related_name="cp_submitter")
	maintainer = models.ForeignKey(User, related_name="cp_maintainer")
	#components may have many footprints associated with them and vice versa
	#but we simply define this in the component model
	footprints = models.ManyToManyField(Footprint, null=True, blank=True)
	

from django.contrib.comments.signals import comment_was_posted
from django.dispatch import receiver

@receiver(comment_was_posted)
def comment_posted_callback(sender, comment, **kwargs):
	''' When a comment is posted, we check if a problem is reported too.'''
	if comment.report_problem:# and (comment.content_object.problem_reported is None):
		comment.problem_object = comment.content_object
		comment.save()
