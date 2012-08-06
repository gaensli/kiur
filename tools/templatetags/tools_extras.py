from django import template
from libmods.models import Component, Footprint

register = template.Library()

@register.inclusion_tag("tools/basket.html", takes_context=True)
def render_basket(context):
	cps = len(filter(lambda x: type(x) == Component, context["basket"]))
	fps = len(filter(lambda x: type(x) == Footprint, context["basket"]))
	if cps == 1:
		cplural = ""
	else:
		cplural = "s"
	if fps == 1:
		fplural = ""
	else:
		fplural = "s"
	is_empty = (cps + fps) == 0
	return {"is_empty":is_empty, "cplural": cplural, "components": cps, "fplural": fplural, "footprints": fps}

@register.filter
def basket_to_numbers (basket):
	cps = len(filter(lambda x: type(x) == Component, basket))
	fps = len(filter(lambda x: type(x) == Footprint, basket))
	if cps == 1:
		l = " components and "
	else:
		l = " components and "
	if fps == 1:
		m = " footprint"
	else:
		m = " footprints"
	return str(cps) + l +  str(fps) + m
