from django.db import models
from django.utils import encoding
from django.contrib.auth.models import User

from easy_thumbnails.signals import saved_file
from easy_thumbnails.signal_handlers import generate_aliases_global
saved_file.connect(generate_aliases_global)

from custom_comments.models import CommentWithFlag
from django.contrib.contenttypes import generic

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
	problems_reported = generic.GenericRelation(CommentWithFlag, 
	                                            content_type_field="problem_object_type", 
																							object_id_field="problem_object_id")
	def get_fields(self):
		return [(field.name, field.value_to_string(self)) for field in self._meta.fields]

	class Meta:
		abstract = True
	def __unicode__(self):
		return self.name

class Footprint(LibMod):
	submitter = models.ForeignKey(User, related_name="fp_submitter")
	maintainer = models.ForeignKey(User, related_name="fp_maintainer")

class Component(LibMod):
	submitter = models.ForeignKey(User, related_name="cp_submitter")
	maintainer = models.ForeignKey(User, related_name="cp_maintainer")
	footprints = models.ManyToManyField(Footprint, null=True, blank=True)
	

from django.contrib.comments.signals import comment_was_posted
from django.dispatch import receiver

@receiver(comment_was_posted)
def comment_posted_callback(sender, comment, **kwargs):
	if comment.report_problem:# and (comment.content_object.problem_reported is None):
		comment.problem_object = comment.content_object
		comment.save()
