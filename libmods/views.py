from django.shortcuts import render_to_response, get_object_or_404
from django.template.context import RequestContext
from libmods.models import Footprint, Component
from urllib import unquote
from kiur.haystack_forms import CustomSearchForm
from haystack.views import SearchView, search_view_factory
from django import forms
from kiur.views import get_session_context

def cmp_detail(request, url_cmp_name):
	extra_context = get_session_context(request)
	extra_context["component"] = get_object_or_404(Component, name=unquote(url_cmp_name))
	return render_to_response("libmods/cmp_detail.html", context_instance=RequestContext(request, extra_context))

def ftp_detail(request, url_ftp_name):
	extra_context = get_session_context(request)
	extra_context["footprint"] = get_object_or_404(Footprint, name=unquote(url_ftp_name))
	return render_to_response("libmods/ftp_detail.html", context_instance=RequestContext(request, extra_context))

