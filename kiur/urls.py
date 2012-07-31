from django.conf.urls import patterns, include, url

from haystack.forms import ModelSearchForm
from haystack.query import SearchQuerySet
from haystack.views import SearchView, search_view_factory

import settings

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()
#import operator
#from haystack.views import SearchView
#from haystack.query import SearchQuerySet, SQ
#from django.conf.urls import patterns, url
#
sqs = SearchQuerySet() # edit remove line that was incorret
#sqs = SearchQuerySet().filter(name_auto=request.GET.get('q', '')
##sqs = SearchQuerySet().filter(reduce(operator.__and__, [SQ(name=word.strip()) for word in query.split(' ')]))
#urlpatterns = patterns('haystack.views',
#    url(r'^$', SearchView(load_all=False,searchqueryset=sqs),name='haystack_search'), 
#)
#sqs = SearchQuerySet()#.filter(author='john')

urlpatterns = patterns('',
    # Examples:
    #url(r'^$', 'kiur.views.index', name='index'),
		#url(r'^$', include('haystack.urls')),
		#url(r'^$', 'kiur.views.SearchWithRequest'),
		url(r'^$', "kiur.views.SearchWithRequest",name='haystack_search'),
    #url(r'^$', search_view_factory(
    #    view_class=SearchView,
    #    template='index.html',
    #    searchqueryset=sqs,
    #    form_class=ModelSearchForm
    #), name='haystack_search'),
    # url(r'^kiur/', include('kiur.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),

		url(r'^search/', include('haystack.urls')),

		url(r"^libs/", include("libmods.urls")),

)


if settings.DEBUG:
    # files (images, css, javascript, etc.)
    urlpatterns += patterns('',
        (r'^media/(?P<path>.*)$', 'django.views.static.serve', {
        'document_root': settings.MEDIA_ROOT}))
