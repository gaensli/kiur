from django.contrib import admin
from custom_comments.models import CommentWithFlag


class CommentWithFlagAdmin(admin.ModelAdmin):
	pass

admin.site.register(CommentWithFlag, CommentWithFlagAdmin)
