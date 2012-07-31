from django import forms
from haystack import site as haystack_site
from haystack.forms import HighlightedSearchForm, model_choices
from django.utils.text import capfirst
from django.utils.encoding import smart_unicode
from django.utils.translation import ugettext_lazy as _
#from haystack.forms import model_choices
from django.db import models

def model_choices(site=None):
	if site is None:
		site = haystack_site

	choices = [("%s.%s" % (m._meta.app_label, m._meta.module_name), smart_unicode(m._meta.verbose_name_plural)) for m in site.get_indexed_models()]
	choices.append(("", "everything"))
	return reversed(choices)

class CustomSearchForm(HighlightedSearchForm):
	def __init__(self, *args, **kwargs):
		super(CustomSearchForm, self).__init__(*args, **kwargs)
		self.fields['models'] = forms.ChoiceField(choices=model_choices(), required=False, label=('Search In'), widget=forms.RadioSelect(attrs={"onclick": "this.form.submit();"}))

	def get_models(self):
		"""Return a list of model classes in the index."""
		search_models = []
		if self.is_valid():
			if not (self.cleaned_data["models"] == ""):
				search_models.append(models.get_model(*self.cleaned_data["models"].split('.')))

		return search_models

	def search(self):
		sqs = super(CustomSearchForm, self).search()
		return sqs.models(*self.get_models())
