from django.conf.urls import patterns, include, url
from shorter import views

urlpatterns = patterns("",
	url(r"^$", views.index, name="index"),
	url(r"^(?P<tinyurl>[^/]+)[/]?$", views.url, name="url"),
)
