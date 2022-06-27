from django.shortcuts import render, redirect
from django.contrib.auth.models import User, Group
from django.urls import reverse
from django.http import HttpResponse, JsonResponse
from django.core.serializers import serialize
from django.template import loader
from django.contrib.auth import login, authenticate  # add this
from django.contrib import messages
from django.contrib.auth.forms import AuthenticationForm  # add this
from django.contrib.auth.decorators import login_required
from gns3webadmin.models import Connection
from gns3fy import Gns3Connector, Project
from .forms import ProjectForm
import json
from my_helpers import dd, any_to_json
import requests


@login_required(login_url='/login')
def projectList(request, connection_id):
    template = loader.get_template('projects.html')
    connection = Connection.objects.get(id=connection_id)
    url = f"http://{connection.ip_address}:{connection.port}"
    try:
        requests.adapters.DEFAULT_RETRIES = 5
        s = requests.session()
        s.keep_alive = False
        s.get(url)
    except:
        messages.error(request, f"{url} : GNS3 server is down.")
        return redirect("/connections")
    server = Gns3Connector(url)
    projects_list = server.get_projects()
    context = {
        'projects_list': projects_list,
        'connection': connection,
        'connection_id': connection_id,
    }
    return HttpResponse(template.render(context, request))


@login_required(login_url='/login')
def projectCreate(request, connection_id):
    connection = Connection.objects.get(id=connection_id)
    url = f"http://{connection.ip_address}:{connection.port}"
    try:
        requests.adapters.DEFAULT_RETRIES = 5
        s = requests.session()
        s.keep_alive = False
        s.get(url)
    except:
        messages.error(request, f"{url} : GNS3 server is down.")
        return redirect("/connections")
    server = Gns3Connector(url)
    if request.method == "POST":
        form = ProjectForm(request.POST)
        if form.is_valid():
            try:
                server.create_project(name=request.POST['name'])
                messages.success(request, "Element created with success")
                found = reverse('project-list', kwargs={'connection_id': connection_id})
                return redirect(found)
            except Exception as e:
                print(e)
                messages.error(request, e)
                found = reverse('project-list', kwargs={'connection_id': connection_id})
                return redirect(found)
        else:
            messages.error(request, list(form.errors.items())[0][1][0])
            found = reverse('project-list', kwargs={'connection_id': connection_id})
            return redirect(found)

    # else:  
    #     form = ProjectForm()  
    # return render(request,'book-create.html',{'form':form})  


@login_required(login_url='/login')
def projectUpdate(request, connection_id, id):
    connection = Connection.objects.get(id=connection_id)
    url = f"http://{connection.ip_address}:{connection.port}"
    try:
        requests.adapters.DEFAULT_RETRIES = 5
        s = requests.session()
        s.keep_alive = False
        s.get(url)
    except:
        messages.error(request, f"{url} : GNS3 server is down.")
        return redirect("/connections")
    server = Gns3Connector(url)
    project = Project(project_id=id, connector=server)
    project.get()
    # raise Exception(project)
    form = ProjectForm(initial={'name': project.name})
    if request.method == "POST":
        form = ProjectForm(request.POST)
        if form.is_valid():
            try:
                project.update(name=request.POST['name'])
                messages.success(request, "Element updated with success")
                found = reverse('project-list', kwargs={'connection_id': connection_id})
                return redirect(found)
            except Exception as e:
                raise e
        else:
            print(list(form.errors.items())[0][1][0])
            messages.error(request, list(form.errors.items())[0][1][0])
            found = reverse('project-list', kwargs={'connection_id': connection_id})
            return redirect(found)
    else:
        data = project.__dict__
        # raise Exception(json.dumps(data, default=lambda o: '<not serializable>'))
        return HttpResponse(any_to_json(data), content_type="application/json")


@login_required(login_url='/login')
def projectDelete(request, connection_id, id):
    connection = Connection.objects.get(id=connection_id)
    url = f"http://{connection.ip_address}:{connection.port}"
    try:
        requests.adapters.DEFAULT_RETRIES = 5
        s = requests.session()
        s.keep_alive = False
        s.get(url)
    except:
        messages.error(request, f"{url} : GNS3 server is down.")
        return redirect("/connections")
    server = Gns3Connector(url)
    try:
        server.delete_project(id)
        messages.success(request, "Element deleted with success")
    except:
        pass
    found = reverse('project-list', kwargs={'connection_id': connection_id})
    return redirect(found)
