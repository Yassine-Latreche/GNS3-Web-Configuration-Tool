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
from gns3fy import Gns3Connector, Project, Node, Link
from .forms import LinkForm
import json
from my_helpers import dd, any_to_json
import requests

# Create your views here.
@login_required(login_url='/login')
def linkIndex(request, connection_id, project_id):
    template = loader.get_template('link_device_index.html')
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
        "started" : 0,
        "suspended" : 0,
        "stopped" : 0
    }
    templates = {}
    nodes_names = {}
    nodes_ports = {}
    for node in nodes:
        # raise Exception(node.template)
        if node.console_type == 'none':
            node.update(console_type="telnet", console_auto_start=True)
            node.reload()
        stats[node.status] += 1
        templates[node.template_id] = server.get_template(template_id=node.template_id)["category"].capitalize()
        nodes_names[node.node_id] = node.name
        nodes_ports[node.node_id] = {}
        # for i in node.ports:
            
    context = {
        'project' : project,
        'connection' : connection,
        'nodes_list' : nodes,
        'nodes_names' : nodes_names,
        'templates_dict' : templates,
        'links_list': links, 
        'stats' : stats,
        'project_id' : project_id,
        'connection_id' : connection_id,
    }
    return HttpResponse(template.render(context, request))

@login_required(login_url='/login')
def linkCreate(request, connection_id, project_id):
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
        form = LinkForm(request.POST)  
        if form.is_valid():  
            try:
                port_a = request.POST['port_a_id'].split("/")
                port_b = request.POST['port_b_id'].split("/")
                port_nodes = [
                    dict(node_id=port_a[0], adapter_number=int(port_a[1]), port_number=int(port_a[2])),
                    dict(node_id=port_b[0], adapter_number=int(port_b[1]), port_number=int(port_b[2])),
                ]
                link = Link(project_id=project_id, connector=server, nodes=port_nodes)
                link.create()
                messages.success(request, "Element created with success")
                found = reverse('device-link-index', kwargs={'connection_id': connection_id, 'project_id': project_id})
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
        template = loader.get_template('new_link.html')
        ports = []
        for node in nodes:
            for link in node.ports:
                ports.append({
                    "node_id": node.node_id,
                    "node_name": node.name,
                    "adapter_number": link["adapter_number"],
                    "port_number": link["port_number"],
                    "name": link["name"],
                })
        context = {
            'project' : project,
            'connection' : connection,
            'nodes_list' : nodes,
            'ports_list' : ports,
            'templates_list' : templates,
            'project_id' : project_id,
            'connection_id' : connection_id,
        }
    return HttpResponse(template.render(context, request))

@login_required(login_url='/login')
def deleteLink(request, connection_id, project_id, link_id):
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
    link = Link(project_id=project_id, link_id=link_id, connector=server)
    link.get()
    try:
        link.delete()
        messages.success(request, "Element deleted with success")
        return redirect(request.META.get('HTTP_REFERER'))
    except Exception as e:
        messages.error(request, f"{e}")
        return redirect(request.META.get('HTTP_REFERER'))