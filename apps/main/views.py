# - - - - - DEPENDENCIES - - - - -

from django.shortcuts import render, redirect
from .models import Email

# - - - - - HELPER FUNCTIONS - - - - -

# Function for initializing session variables.
def seshinit(request, sesh, val=''):
	if sesh not in request.session:
		request.session[sesh] = val
	return request.session[sesh]

# Function to copy keys/value pairs from one dict into another
def copy(source, keys=False):
	this = {}
	if not keys:
		keys = source.keys()
	for key in keys:
		this[key] = source[key]
	return this

# - - - - - DEVELOPER VIEWS - - - - -

def hot(request):
	seshinit(request,'command')
	context = {
		# Models
		'command': request.session['command']
	}
	return render(request, "main/hot.html", context)

def run(request):
	command = request.POST['command']
	request.session['command'] = command
	exec(command)
	return redirect ('/hot')

def nuke(request):
	#.objects.all().delete()
	request.session.clear()
	return redirect ('/hot')

# - - - - - APPLICATION VIEWS - - - - -

def index(request):
	context = {
		'redbox': seshinit(request,'redbox','none'),
		'errors': seshinit(request,'errors',[]),
		'emails': Email.objects.all(),
	}
	return render(request, "main/index.html", context)

def process(request):
	data = copy(request.POST, ['email'])
	print data
	if Email.objects.isValid(data):
		print "Valid"
		Email.objects.create(data)
		request.session['redbox'] = 'none'
	else:
		print "Invalid"
		request.session['redbox'] = 'inline-block'
		request.session['errors'] = Email.objects.errors(data)
	return redirect ('/')




