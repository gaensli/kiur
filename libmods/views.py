from django.shortcuts import render, get_object_or_404
from django.template.context import RequestContext
from urllib import unquote
from kiur.haystack_forms import CustomSearchForm
from haystack.views import SearchView, search_view_factory
from django import forms
from kiur.views import get_session_context
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect, Http404

import libmods.parse as parse

from libmods.models import Footprint, Component
from libmods.forms import UploadFormOne, UploadFormLib, UploadFormDcm, UploadFormWrl, UploadFormMod

def cmp_detail(request, url_cmp_name):
	extra_context = get_session_context(request)
	extra_context["component"] = get_object_or_404(Component, name=unquote(url_cmp_name))
	extra_context["next"] = "/components/" + url_cmp_name + "/"
	return render(request, "libmods/cmp_detail.html", extra_context)

def ftp_detail(request, url_ftp_name):
	extra_context = get_session_context(request)
	extra_context["footprint"] = get_object_or_404(Footprint, name=unquote(url_ftp_name))
	extra_context["next"] = "/components/" + url_ftp_name + "/"
	return render(request, "libmods/ftp_detail.html", extra_context)

@login_required
def submit(request, step):
	step = int(step)
	extra_context = get_session_context(request)
	if step == 1:
		extra_context["upload_form"] =  UploadFormOne()
		extra_context["redirect"] = "/submit/2/"
		return render(request, "submit.html", extra_context)
	elif step == 2:
		form = UploadFormOne(request.POST, request.FILES)
		if form.is_valid():
			try:
				parse_context = parse.parse_uploaded_file(request)
				extra_context.update(parse_context)
			except parse.ParseFailed as e:
				extra_context["upload_form"] =  UploadFormOne()
				extra_context["redirect"] = "/submit/2/"
				extra_context["error_message"] = e
				return render(request, "submit.html", extra_context)
			else: 
				extra_context["redirect"] = "/submit/3/"#?t=" + form.kind
				return render(request, "submit.html", extra_context)
		else:
			extra_context["upload_form"] =  UploadFormOne()
			extra_context["redirect"] = "/submit/2/"
			extra_context["error_message"] = "Invalid upload file" 
			return render(request, "submit.html", extra_context)

	elif step == 3:
		pass
	else:
		raise Http404
