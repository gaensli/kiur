from django.shortcuts import render, get_object_or_404
from django.template.context import RequestContext
from django.http import HttpResponseRedirect
from django.http import HttpResponseNotAllowed
from django.http import HttpResponse
import ast 

from haystack.views import SearchView, search_view_factory
from haystack.query import SearchQuerySet 
#from haystack.forms import HighlightedModelSearchForm, ModelSearchForm, FacetedSearchForm
from kiur.haystack_forms import CustomSearchForm
from django.contrib.auth.views import login as djlogin
from libmods.models import Component, Footprint

import json

def get_session_form(request):
	try:
		form = CustomSearchForm(request.session["last_search"])
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
			data["libs"] = len(filter(lambda x: isinstance(x, Component), basket))
			data["mods"] = len(filter(lambda x: isinstance(x, Footprint), basket))
			data["success"] = True
			return HttpResponse(json.dumps(data), mimetype="application/json")
		else:
			try:
				q = request.session["last_search"]["q"]
			except:
				q = ""
			try:
				models = request.session["last_search"]["models"]
			except:
				models = ""
			try:
				page = request.session["last_search"]["page"]
			except:
				page = "1"
			return HttpResponseRedirect("/search/?q="+ q +"&models=" +  models + "&page=" + page)
	else:
		#XXX should check for request.GET but it doesn't seem to work..
		if request.is_ajax():
			basket = request.session["basket"]
			data = {}
			data["libs"] = len(filter(lambda x: type(x) is Component, basket))
			data["mods"] = len(filter(lambda x: type(x) is Footprint, basket))
			data["success"] = True
			return HttpResponse(json.dumps(data), mimetype="application/json")
		return HttpResponseNotAllowed(request)

from django.core.servers.basehttp import FileWrapper
import os
import tempfile
from django.core.files.temp import NamedTemporaryFile

def download(request):
	#TODO make a file in /tmp/ and let apache serve it
	if request.POST:
		p = request.POST
		f = tempfile.NamedTemporaryFile()
		if p["_type"] == "Component":
			libmod = get_object_or_404(Component, name=p["libmod"])
			name = p["libmod"] + ".lib"
			version = ast.literal_eval(libmod.ki_version)
			f.write("EESchema-LIBRARY Version "+ ".".join(version) + "\n")
		elif p["_type"] == "Footprint":
			name = p["libmod"] + ".mod"
			libmod = get_object_or_404(Footprint, p["libmod"])

		f.write(libmod.ki_text)
		f.seek(0)
		response = HttpResponse(FileWrapper(f), content_type='text/plain')
		#response['Content-Length'] = os.path.getsize(f)
		response['Content-Disposition'] = "attachment; filename=" + name
		return response


		

def search(request):
	request.session["last_search"] = request.GET
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
	
