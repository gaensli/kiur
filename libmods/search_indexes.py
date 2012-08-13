import datetime
from haystack.indexes import RealTimeSearchIndex 
from haystack import site, indexes
from libmods.models import Component, Footprint

class LibModIndex(RealTimeSearchIndex):
	#the templates are templates/search/indexes/libmods/component_content_auto.txt
	#and footprint_content_auto.txt
	content_auto = indexes.EdgeNgramField(document=True, use_template=True)
	#content_auto = CharField(document=True, use_template=True)
	#def index_queryset(self):
	#	return Component.objects.filter(date_added__lte=datetime.datetime.now())

site.register(Component, LibModIndex)
site.register(Footprint, LibModIndex)
