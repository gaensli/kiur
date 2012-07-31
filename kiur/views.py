#from django.shortcuts import render_to_response
#from django.template.context import RequestContext
#from libmods.models import Footprint, Component
#
#def index(request):
#	fp = Footprint.objects.all().order_by("-date_added")[:5]
#	cp = Component.objects.all().order_by("-date_added")[:5]
#	return render_to_response("index.html", context_instance=RequestContext(request, {"latest_footprints":fp, "latest_components":cp}))
from haystack.views import SearchView, search_view_factory
from haystack.query import SearchQuerySet 
from haystack.forms import HighlightedModelSearchForm
from kiur.haystack_forms import CustomSearchForm

def SearchWithRequest(request):
	sqs = SearchQuerySet().filter(content_auto=request.GET.get('q', ''))
	#sqs = SearchQuerySet().autocomplete(name_auto='tes')
	#sqs = SearchQuerySet().filter(code__startswith=request.GET.get('q', ''))
	view = search_view_factory(
		view_class=SearchView,
		template='index.html',
		searchqueryset=sqs,
		#form_class=CustomSearchForm
		form_class=HighlightedModelSearchForm
		)
	return view(request)

#class SearchWithRequest(SearchView):
#	def __name__(self):
#		return "SearchWithRequest"
#
#	def build_form(self, form_kwargs=None):
#		if form_kwargs is None:
#			form_kwargs = {}
#
#		if self.searchqueryset is None:
#			sqs = SearchQuerySet().filter(name_auto=self.request.GET.get('q', ''))
#			form_kwargs["searchqueryset"] = sqs
#
#		return super(SearchWithRequest, self).build_form(form_kwargs)
