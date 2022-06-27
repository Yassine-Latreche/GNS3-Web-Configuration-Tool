from pprint import pprint
from django.shortcuts import render, redirect
from django.contrib.auth.models import User, Group
from django.urls import reverse
from django.http import HttpResponse, JsonResponse
from django.core.serializers import serialize
from django.template import loader
from django.contrib.auth import login, authenticate #add this
from django.contrib import messages
from django.contrib.auth.forms import AuthenticationForm #add this
from django.contrib.auth.decorators import login_required
from gns3webadmin.models import Connection
from gns3fy import Gns3Connector, Project, Node
from device.forms import DeviceForm
import json
from my_helpers import dd, any_to_json
import requests

@login_required(login_url='/login')
def projectMainDashboard(request, connection_id, project_id):
    template = loader.get_template('index.html')
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
    project = Project(project_id=project_id, connector=server)
    project.get()
    project.open()
    nodes = project.nodes
    links = project.links
    stats = {
        "started" : 0,
        "suspended" : 0,
        "stopped" : 0
    }
    templates = {}
    for node in nodes:
        # raise Exception(node.template)
        if node.console_type == 'none':
            node.update(console_type="telnet", console_auto_start=True)
            node.reload()
        stats[node.status] += 1
        templates[node.template_id] = server.get_template(template_id=node.template_id)["category"].capitalize()
    # nodes_list = [any_to_json(x.__dict__) for x in nodes]
    # links_list = [any_to_json(x.__dict__) for x in links]
    context = {
        'project' : project,
        'connection' : connection,
        'nodes_list' : nodes,
        'templates_dict' : templates,
        # 'links_list': links_list, 
        'stats' : stats,
        'project_id' : project_id,
        'connection_id' : connection_id,
    }
    return HttpResponse(template.render(context, request))

@login_required(login_url='/login')
def projectMainNetwork(request, connection_id, project_id):
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
    project = Project(project_id=project_id, connector=server)
    project.get()
    nodes = project.nodes
    links = project.links
    stats = {
        "nodes" : [{
            "node_id" : n.node_id, 
            "name" : n.name, 
            "node_type" : n.node_type,
            "status" : n.status,
            "console" : n.console,
            "x" : n.x,
            "y" : n.y,
            "console_host" : n.console_host,
            "console_type" : n.console_type,
            "symbol" : f"http://{connection.ip_address}:{connection.port}/v2/symbols/{n.symbol}/raw",
        } for n in nodes],
        "links" : [{
            "link" : [l.__dict__[v] for v in l.__dict__],
            "link_id" : l.link_id, 
            "link_type" : l.link_type, 
            "source" : l.nodes[0]["node_id"],
            "source_port" : l.nodes[0]["port_number"],
            "target" : l.nodes[1]["node_id"],
            "target_port" : l.nodes[1]["port_number"],
        } for l in links],
    }
    return HttpResponse(any_to_json(stats), content_type="application/json")
    

@login_required(login_url='/login')
def projectMainCreateDevice(request, connection_id, project_id):
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
    project = Project(project_id=project_id, connector=server)
    project.get()
    nodes = project.nodes
    templates = server.get_templates()
    if request.method == "POST":  
        form = DeviceForm(request.POST)  
        if form.is_valid():  
            try:  
                node = Node(name=request.POST['name'], template_id=request.POST['template_id'], project_id=project_id, connector=server)
                node.create()
                messages.success(request, "Element updated with success")
                found = reverse('project-main-dashboard', kwargs={'connection_id': connection_id, 'project_id': project_id})
                return redirect(found)  
            except Exception as e: 
                messages.error(request, f"{e}")
                # found = reverse('project-main-dashboard', kwargs={'connection_id': connection_id, 'project_id': project_id})
                return redirect(request.META.get('HTTP_REFERER'))  
        else:
            messages.error(request, list(form.errors.items()))
            # found = reverse('project-main-dashboard', kwargs={'connection_id': connection_id, 'project_id': project_id})
            return redirect(request.META.get('HTTP_REFERER'))
    else:
        template = loader.get_template('new_device.html')
        context = {
            'project' : project,
            'connection' : connection,
            'nodes_list' : nodes,
            'templates_list' : templates,
            'project_id' : project_id,
            'connection_id' : connection_id,
        }
    return HttpResponse(template.render(context, request))

@login_required(login_url='/login')
def projectMainOpen(request, connection_id, project_id):
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
    project = Project(project_id=project_id, connector=server)
    try:
        project.open()
        messages.success(request, "Element has been opened with success")
        return redirect(request.META.get('HTTP_REFERER'))
    except Exception as e:
        messages.error(request, f"{e}")
        return redirect(request.META.get('HTTP_REFERER'))

@login_required(login_url='/login')
def projectMainClose(request, connection_id, project_id):
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
    project = Project(project_id=project_id, connector=server)
    try:
        project.close()
        messages.success(request, "Element has been closed with success")
        return redirect(f"/connections/{connection_id}/projects")
    except Exception as e:
        messages.error(request, f"{e}")
        return redirect(request.META.get('HTTP_REFERER'))