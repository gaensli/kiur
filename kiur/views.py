from django.shortcuts import render, get_object_or_404
from django.template.context import RequestContext
from django.http import HttpResponseRedirect
from django.http import HttpResponseNotAllowed
from django.http import HttpResponse

from haystack.views import SearchView, search_view_factory
from haystack.query import SearchQuerySet 
#from haystack.forms import HighlightedModelSearchForm, ModelSearchForm, FacetedSearchForm
from kiur.haystack_forms import CustomSearchForm
from django.contrib.auth.views import login as djlogin
from libmods.models import Component, Footprint

import json

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
	user = request.user;
	return {"form": form, "basket": basket, "user":user}

def index(request):
	form = CustomSearchForm()
	basket = get_session_basket(request)
	return render(request, "index.html", {"form": form, "basket": basket})

def _modify_basket(request, libmod):
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

def modify_basket(request):
	if request.POST:
		p = request.POST
		try:
			if p["_type"] == "Component":
				libmod = Component.objects.get(name=p["libmod"])
			elif p["_type"] == "Footprint":
				libmod = Footprint.objects.get(name=p["libmod"])
			else:
				print p["_type"]
				raise TypeError

			_modify_basket(request, libmod)
		except:
			if request.is_ajax():
				data = {"success":False}
				return HttpResponse(json.dumps(data), mimetype="application/json")
		if request.is_ajax():
			basket = request.session["basket"]
			data = {}
			data["in_basket"] = libmod in basket
			data["name"] = p["libmod"]
			data["_type"] = p["_type"]
			data["libs"] = len(filter(lambda x: type(x) is Component, basket))
			data["mods"] = len(filter(lambda x: type(x) is Footprint, basket))
			data["success"] = True
			return HttpResponse(json.dumps(data), mimetype="application/json")
		else:
			try:
				q = request.session["last_get"]["q"]
			except:
				q = ""
			try:
				models = request.session["last_get"]["models"]
			except:
				models = ""
			try:
				page = request.session["last_get"]["page"]
			except:
				page = "1"
			return HttpResponseRedirect("/search/?q="+ q +"&models=" +  models + "&page=" + page)
	else:
		print request.GET
		if request.is_ajax():
			basket = request.session["basket"]
			data = {}
			data["libs"] = len(filter(lambda x: type(x) is Component, basket))
			data["mods"] = len(filter(lambda x: type(x) is Footprint, basket))
			data["success"] = True
			return HttpResponse(json.dumps(data), mimetype="application/json")
		return HttpResponseNotAllowed(request)

def search(request):
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
	
