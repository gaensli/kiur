from django.shortcuts import render_to_response, get_object_or_404
from django.template.context import RequestContext
from libmods.models import Footprint, Component
from urllib import unquote

def cmp_detail(request, url_cmp_name):
	cp = get_object_or_404(Component, name=unquote(url_cmp_name))
	return render_to_response("libmods/cmp_detail.html", context_instance=RequestContext(request, {"component":cp,}))
