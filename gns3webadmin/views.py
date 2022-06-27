from django.db import connection
from django.shortcuts import render, redirect
from django.contrib.auth.models import User, Group
from django.urls import reverse
from django.http import HttpResponse
from django.core.serializers import serialize
from django.template import loader
from django.contrib.auth import login, authenticate #add this
from django.contrib import messages
from django.contrib.auth.forms import AuthenticationForm #add this
from django.contrib.auth.decorators import login_required

from rest_framework import permissions
from rest_framework import viewsets

from gns3webadmin.serializers import UserSerializer, GroupSerializer, ConnectionSerializer
from .forms import NewUserForm
from gns3webadmin.models import Connection
from .forms import ConnectionForm

def register_request(request):
	if request.method == "POST":
		form = NewUserForm(request.POST)
		if form.is_valid():
			user = form.save()
			login(request, user)
			messages.success(request, "Registration successful." )
			return redirect("connections")
		messages.error(request, "Unsuccessful registration. Invalid information.")
	form = NewUserForm()
	return render (request=request, template_name="auth/register.html", context={"register_form":form})


def login_request(request):
	if request.method == "POST":
		form = AuthenticationForm(request, data=request.POST)
		if form.is_valid():
			username = form.cleaned_data.get('username')
			password = form.cleaned_data.get('password')
			user = authenticate(username=username, password=password)
			if user is not None:
				login(request, user)
				messages.info(request, f"You are now logged in as {username}.")
				return redirect("connections")
			else:
				messages.error(request,"Invalid username or password.")
		else:
			messages.error(request,"Invalid username or password.")
	form = AuthenticationForm()
	return render(request=request, template_name="auth/login.html", context={"login_form":form})

@login_required(login_url='/login')
def index(request):
	template = loader.get_template('connections.html')
	connections_list = Connection.objects.all()
	context = {
		'connections_list' : connections_list,
	}
	return HttpResponse(template.render(context, request))

@login_required(login_url='/login')
def connectionList(request):
	template = loader.get_template('connections.html')
	connections_list = Connection.objects.all()
	context = {
		'connections_list' : connections_list,
	}
	return HttpResponse(template.render(context, request))

@login_required(login_url='/login')
def connectionCreate(request):  
	if request.method == "POST":  
		form = ConnectionForm(request.POST)  
		if form.is_valid():  
			try:  
				form.save() 
				model = form.instance
				messages.success(request, "Element created with success")
				return redirect('connection-list')  
			except:  
				pass 
		else:
			print(list(form.errors.items())[0][1][0])
			messages.error(request, list(form.errors.items())[0][1][0])
			found = reverse('connection-list')
			return redirect(found)

	# else:  
	#	 form = ConnectionForm()  
	# return render(request,'book-create.html',{'form':form})  

@login_required(login_url='/login')
def connectionUpdate(request, id):  
	connection = Connection.objects.get(id=id)
	form = ConnectionForm(initial={'ip_address': connection.ip_address, 'port': connection.port})
	if request.method == "POST":  
		form = ConnectionForm(request.POST, instance=connection)  
		if form.is_valid():  
			try:  
				form.save() 
				model = form.instance
				messages.success(request, "Element updated with success")
				return redirect('connection-list')  
			except Exception as e: 
				pass
		else:
			print(list(form.errors.items())[0][1][0])
			messages.error(request, list(form.errors.items())[0][1][0])
			found = reverse('connection-list')
			return redirect(found)
	else:
		data = serialize("json", [connection], fields=('ip_address', 'port'))
		return HttpResponse(data, content_type="application/json")

@login_required(login_url='/login')
def connectionDelete(request, id):
	connection = Connection.objects.get(id=id)
	try:
		connection.delete()
		messages.success(request, "Element deleted with success")
	except:
		pass
	return redirect('connection-list')

class UserViewSet(viewsets.ModelViewSet):
	"""
	API endpoint that allows users to be viewed or edited.
	"""
	queryset = User.objects.all().order_by('-date_joined')
	serializer_class = UserSerializer
	permission_classes = [permissions.IsAuthenticated]


class GroupViewSet(viewsets.ModelViewSet):
	"""
	API endpoint that allows groups to be viewed or edited.
	"""
	queryset = Group.objects.all()
	serializer_class = GroupSerializer
	permission_classes = [permissions.IsAuthenticated]

class ConnectionViewSet(viewsets.ModelViewSet):
	"""
	API endpoint that allows connections to be viewed or edited.
	"""
	queryset = Connection.objects.all()
	serializer_class = ConnectionSerializer
	permission_classes = [permissions.IsAuthenticated]