from django.core import serializers
from collections.abc import Iterable
from django.db.models.query import QuerySet
from django.core.exceptions import ObjectDoesNotExist
import json
from netaddr import IPAddress
from telnetlib import Telnet
import time
def dd(request, data=''):
    try:
        scheme      = request.scheme
        server_name = request.META['SERVER_NAME']
        server_port = request.META['SERVER_PORT']
        remote_addr = request.META['REMOTE_ADDR']
        user_agent  = request.META['HTTP_USER_AGENT']
        path        = request.path
        method      = request.method
        session     = request.session
        cookies     = request.COOKIES

        get_data = {}
        for key, value in request.GET.lists():
            get_data[key] = value

        post_data = {}
        for key, value in request.POST.lists():
            post_data[key] = value

        files = {}
        for key, value in request.FILES.lists():
            files['name'] = request.FILES[key].name
            files['content_type'] = request.FILES[key].content_type
            files['size'] = request.FILES[key].size

        dump_data = ''
        query_data = ''
        executed_query = ''
        if data:
            if isinstance(data, Iterable):
                if isinstance(data, QuerySet):
                    executed_query = data.query
                    query_data = serializers.serialize('json', data)
                else:
                    try:
                        dump_data = dict(data)
                    except:
                        dump_data = data
            else:
                query_data = serializers.serialize('json', [data])


        msg = f'''
            <html>
                <span style="color: red;"><b>Scheme</b></span>        : <span style="color: blue;">{scheme}</span><br>
                <span style="color: red;"><b>Server Name</b></span>   : <span style="color: blue;">{server_name}</span><br>
                <span style="color: red;"><b>Server Port</b></span>   : <span style="color: blue;">{server_port}</span><br>
                <span style="color: red;"><b>Remote Address</b></span>: <span style="color: blue;">{remote_addr}</span><br>
                <span style="color: red;"><b>User Agent</b></span>    : <span style="color: blue;">{user_agent}</span><br>
                <span style="color: red;"><b>Path</b></span>          : <span style="color: blue;">{path}</span><br>
                <span style="color: red;"><b>Method</b></span>        : <span style="color: blue;">{method}</span><br>
                <span style="color: red;"><b>Session</b></span>       : <span style="color: blue;">{session}</span><br>
                <span style="color: red;"><b>Cookies</b></span>       : <span style="color: blue;">{cookies}</span><br>
                <span style="color: red;"><b>Get Data</b></span>      : <span style="color: blue;">{get_data}</span><br>
                <span style="color: red;"><b>Post Data</b></span>     : <span style="color: blue;">{post_data}</span><br>
                <span style="color: red;"><b>Files</b></span>         : <span style="color: blue;">{files}</span><br>
                <span style="color: red;"><b>Executed Query</b></span>: <span style="color: blue;"><br>{executed_query}</span><br>
                <span style="color: red;"><b>Query Data</b></span>    : <span style="color: blue;"><br>{query_data}</span><br>
                <span style="color: red;"><b>Dump Data</b></span>     : <span style="color: blue;"><br>{dump_data}</span><br>
            </html>
        '''

        return msg
    except ObjectDoesNotExist:
        return False

def any_to_json(data):
    return json.dumps(data, default=lambda o: '<not serializable>')

def prepareTelnet(tn, cmd):
    # tn = Telnet(str(device.console_host), device.console)
    if cmd == "connect":
        tn.write(b'\r')
        tn.read_until(b"#").decode("utf-8")
        # tn.write(b'\x15')
        # tn.read_until(b"#").decode("utf-8")
    else:
        # tn.write(b'exit')
        # print(tn.read_until("").decode("utf-8"))
        tn.close()

def getVlansFromOutput(output):
    list = [x.split(" ")[0] for x in output.split("\n")][2:]
    return list

def sendGuestIpAddress(tn, ipAddress, mask, defaultGateway):
    # tn = Telnet(str(device.console_host), device.console)
    tn.write(b'\r')
    tn.read_until(b">").decode("utf-8")
    cmd = f"ip {ipAddress}/{IPAddress(mask).netmask_bits()} {defaultGateway}".encode()
    tn.write(cmd+b"\r\n")
    tn.write(b'\r')
    tn.read_until(b">").decode("utf-8")
    # tn.write(b'\x15')
    # tn.read_until(b"#").decode("utf-8")
    time.sleep(2)
    tn.close()

def guestShowIp(tn):
    tn.write(b'\r')
    tn.read_until(b">").decode("utf-8")
    tn.write(b"show ip\r")
    res = tn.read_until(b">").decode("utf-8")
    time.sleep(2)
    tn.close()
    return res

def guestPing(tn, ipAddress):
    tn.write(b'\r')
    tn.read_until(b">").decode("utf-8")
    cmd = f"ping {ipAddress}".encode()
    tn.write(cmd + b"\r")
    res = tn.read_until(b">").decode("utf-8")
    time.sleep(2)
    tn.close()
    return res
