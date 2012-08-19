from django.db import models
from django.contrib.comments.models import Comment

class CommentWithFlag(Comment):
	flag = models.BooleanField()
