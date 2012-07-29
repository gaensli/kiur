from django.shortcuts import render_to_response
from django.template.context import RequestContext
from libmods.models import Footprint, Component

def index(request):
	fp = Footprint.objects.all().order_by("-date_added")[:5]
	cp = Component.objects.all().order_by("-date_added")[:5]
	return render_to_response("index.html", context_instance=RequestContext(request, {"latest_footprints":fp, "latest_components":cp}))
