import datetime
from haystack.indexes import *
from haystack import site
from libmods.models import Component

class ComponentIndex(SearchIndex):
	name = CharField(document=True, use_template=True)
	date_added = DateTimeField(model_attr="date_added") 
	def index_queryset(self):
		return Component.objects.filter(date_added__lte=datetime.datetime.now())

site.register(Component, ComponentIndex)
