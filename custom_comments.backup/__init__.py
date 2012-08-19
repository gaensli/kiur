from custom_comments.models import CommentWithFlag
from custom_comments.forms import CommentFormWithFlag

def get_model():
	return CommentWithFlag

def get_form():
	return CommentFormWithFlag
