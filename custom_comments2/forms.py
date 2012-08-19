from django import forms
from django.contrib.comments.forms import CommentForm
from custom_comments.models import CommentWithFlag


class CommentFormWithFlag(CommentForm):
	flag = forms.BooleanField()

	def get_comment_model(self):
		return CommentWithFlag
	
	def get_comment_create_data(self):
		data = super(CommentFormWithFlag, self).get_comment_create_data()
		data["flag"] = self.cleaned_data["flag"]
		return data
	
	
