from django import forms
from django.contrib.comments.forms import CommentForm
from custom_comments.models import CommentWithFlag

from django.contrib.contenttypes.models import ContentType
from django.utils.encoding import force_unicode
from django.conf import settings 
import datetime

class CommentFormWithFlag(CommentForm):
	report_problem = forms.BooleanField(required=False)

	def get_comment_model(self):
		return CommentWithFlag

	def get_comment_create_data(self):
		return dict(
			content_type = ContentType.objects.get_for_model(self.target_object),
			object_pk = force_unicode(self.target_object._get_pk_val()),
			comment  = self.cleaned_data["comment"],
			submit_date = datetime.datetime.now(),
			site_id = settings.SITE_ID,
			is_public = True,
			is_removed = False,
			report_problem = self.cleaned_data["report_problem"]
		)
	
CommentFormWithFlag.base_fields.pop("url")
CommentFormWithFlag.base_fields.pop("name")
CommentFormWithFlag.base_fields.pop("email")
