from django.conf.urls import patterns, include, url

from haystack.forms import ModelSearchForm
from haystack.query import SearchQuerySet
from haystack.views import SearchView, search_view_factory

import settings

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

#sqs = SearchQuerySet() # 

urlpatterns = patterns('',
		
		url(r"^$", "kiur.views.index"),
		#url(r'^search/$', include('haystack.urls')),
		url(r"^search/$", "kiur.views.search"),
    (r'^comments/', include('django.contrib.comments.urls')),
		
		#url(r"^(?P<libmod_type>components)/$",  "kiur.views.SearchWithRequest",name='haystack_search'),
		#url(r"^(?P<libmod_type>footprints)/$",  "kiur.views.SearchWithRequest",name='haystack_search'),

    #url(r'^$', search_view_factory(
    #    view_class=SearchView,
    #    template='index.html',
    #    searchqueryset=sqs,
    #    form_class=ModelSearchForm
    #), name='haystack_search'),

    # Uncomment the admin/doc line below to enable admin documentation:
    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
    url(r'^login/$', "kiur.views.login"),
    url(r'^logout/$', "django.contrib.auth.views.logout"),

		url(r"submit/(?P<step>\d)/$", "libmods.views.submit"), 


		#url(r"^libs/", include("libmods.urls")),
		url(r"^components/(?P<url_cmp_name>[\w\W]+)/$", "libmods.views.cmp_detail"),
		url(r"^footprints/(?P<url_ftp_name>[\w\W]+)/$", "libmods.views.ftp_detail"),
		url(r"^test_basket/$", "kiur.views.test_basket"),
		#url(r"(?P<url_cmp_name>[\w|\W]+)/$", "cmp_detail"),

)


if settings.DEBUG:
    # files (images, css, javascript, etc.)
    urlpatterns += patterns('',
        (r'^media/(?P<path>.*)$', 'django.views.static.serve', {
        'document_root': settings.MEDIA_ROOT}))
