from django.conf.urls import url
from . import views, verbs

urlpatterns = [
	url(r'^$', verbs.index),
	url(r'^hot$', views.hot),
	url(r'^run$', views.run),
]
