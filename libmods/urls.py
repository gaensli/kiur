from django.conf.urls import patterns, url

urlpatterns = patterns("libmods.views",
		url(r"(?P<url_cmp_name>[\w|\W]+)/$", "cmp_detail"),
		#url(r"footprints/(?P<url_ftp_name>[\w|\W]+)/$", "ftp_detail"),
)
