from django.db import models
from django.contrib.comments.models import Comment
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes import generic

class CommentWithFlag(Comment):
	report_problem = models.BooleanField(default=False)
	problem_object_type = models.ForeignKey(ContentType, blank=True, null=True)
	problem_object_id = models.PositiveIntegerField(blank=True, null=True)
	problem_object = generic.GenericForeignKey("problem_object_type", "problem_object_id")
