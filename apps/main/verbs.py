from django.shortcuts import HttpResponse
from . import views

def index(request):
	if request.method == "GET":
		return views.index(request)
	elif request.method == "POST":
		return views.process(request)
	else:
		return HttpResponse("HTTP Verb Not Recognized")
