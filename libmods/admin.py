from libmods.models import Footprint, Component 
from django.contrib import admin
from django.contrib.contenttypes import generic
from custom_comments.models import CommentWithFlag

class ProblemsInline(generic.GenericStackedInline):
	model = CommentWithFlag
	ct_field = "problem_object_type"
	ct_fk_field = "problem_object_id"

class LibModAdmin(admin.ModelAdmin):
	inlines = [
		ProblemsInline,
	]

admin.site.register(Footprint, LibModAdmin)
admin.site.register(Component, LibModAdmin)
