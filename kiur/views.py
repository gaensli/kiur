from django.shortcuts import render, get_object_or_404
from django.template.context import RequestContext
from django.http import HttpResponseRedirect

from haystack.views import SearchView, search_view_factory
from haystack.query import SearchQuerySet 
#from haystack.forms import HighlightedModelSearchForm, ModelSearchForm, FacetedSearchForm
from kiur.haystack_forms import CustomSearchForm
from django.contrib.auth.views import login as djlogin
from libmods.models import Component, Footprint

def get_session_form(request):
	try:
		form = CustomSearchForm(request.session["last_get"])
	except KeyError:
		form = CustomSearchForm()
	return form

def get_session_basket(request):
	try:
		basket = request.session["basket"]
	except KeyError:
		basket = []
	return basket

def get_session_context(request):
	form = get_session_form(request)
	basket = get_session_basket(request)
	return {"form": form, "basket": basket}

def index(request):
	form = CustomSearchForm()
	basket = get_session_basket(request)
	return render(request, "index.html", {"form": form, "basket": basket})

def add_to_basket(request, libmod):
	basket = get_session_basket(request)
	if libmod in basket:
		basket.remove(libmod)
	else:
		basket.append(libmod)
	#uniquify just to be sure
	basket = list(set(basket))
	request.session["basket"] = basket

class CustomSearchView(SearchView):
	def __name__(self):
		return "CustomSearchView"
	
	def extra_context(self):
		extra = super(CustomSearchView, self).extra_context()
		extra["models"] = self.request.GET.get("models", "")
		extra["basket"] = get_session_basket(self.request)
		return extra

def search(request):
	if request.POST:
		if "addcp" in request.GET:
			libmod = Component.objects.get(name=request.GET.get("addcp", ""))
			add_to_basket(request, libmod)
		elif "addfp" in request.GET:
			libmod = Footprint.objects.get(name=request.GET.get("addfp", ""))
			add_to_basket(request, libmod)
		return HttpResponseRedirect("/search/?q=" + request.GET.get('q', '') + "&models=" +  request.GET.get("models", ""))
	else:
		request.session["last_get"] = request.GET
		sqs = SearchQuerySet().filter(content_auto=request.GET.get('q', ''))
		request.session["sqs"] = sqs
		view = search_view_factory(
			view_class=CustomSearchView,
			template="search.html",
			searchqueryset=sqs,
			form_class=CustomSearchForm,
			context_class=RequestContext,
			)
		return view(request)

def login(request):
	return djlogin(request, extra_context=get_session_context(request))
	
