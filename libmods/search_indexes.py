import datetime
from haystack.indexes import *
from haystack import site, indexes
from libmods.models import Component, Footprint

class LibModIndex(SearchIndex):
	#the templates are templates/search/indexes/libmods/component_content_auto.txt
	#and footprint_content_auto.txt
	content_auto = indexes.EdgeNgramField(document=True, use_template=True)
	#def index_queryset(self):
	#	return Component.objects.filter(date_added__lte=datetime.datetime.now())

#class FootprintIndex(SearchIndex):
#	name = CharField(document=True, use_template=True)
#	date_added = DateTimeField(model_attr="date_added") 
#	name_auto = indexes.EdgeNgramField(model_attr='name')
#	def index_queryset(self):
#		return Footprint.objects.filter(date_added__lte=datetime.datetime.now())


site.register(Component, LibModIndex)
site.register(Footprint, LibModIndex)
