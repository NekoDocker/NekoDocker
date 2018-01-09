import time

import re
from django.shortcuts import render_to_response, render
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponseRedirect, HttpResponse, JsonResponse
import json
import requests
from numpy.ma.bench import timer
from containers.tasks import Containers_Cpu,All_Host
from dashboard.models import ip
from containers.models import Info,Cpu_mem

@csrf_exempt
def Containers_info(request):
    ALL = str(request)
    load = {'all':'true'}
    b = ":2375/containers/json"
    Ip = ALL[7 :]
    I = "http://"+Ip+b
    r = requests.get(I,load)
    doc = json.loads(r.text)
    for r in range(0,len(doc)):
        info_db = Info.objects.create()
        info_db.Cid = doc[r]['Id']
        info_db.Name = doc[r]['Names'][0]
        info_db.State = doc[r]['State']
        info_db.Image = doc[r]['Image']
        info_db.Command = doc[r]['Command']
        if (doc[r]['Ports'] != []):
            if(doc[r]['Ports'][0]['PrivatePort']&doc[r]['Ports'][0]['PublicPort']!=[]):
                info_db.PrivatePort = str(doc[r]['Ports'][0]['PrivatePort'])
                info_db.PublicPort = str(doc[r]['Ports'][0]['PublicPort'])
                info_db.Type = str(doc[r]['Ports'][0]['Type'])
        info_db.Ip = Ip
        info_db.save()
    return HttpResponseRedirect("/Containers/")
def Containers(request):
    Ip_get = ip.objects.filter(Ip__contains='http')
    if(Ip_get==''):
        return render_to_response('Containers.html')
    else:
        info = Info.objects.all()
        info.delete()
        for r in range(0,len(Ip_get)) :
            Containers_info(Ip_get[r].Ip)
        return render_to_response('Containers.html',locals())
def Containers_search(request):
    Ip_get = ip.objects.filter(Ip__contains='http')
    if (Ip_get != ''):
        info = Info.objects.all()
        info.delete()
        for r in range(0, len(Ip_get)):
            Containers_info(Ip_get[r].Ip)
    INFO = Info.objects.filter(Cid__contains=request.GET['Cid'])
    if(INFO == ''):
        return HttpResponseRedirect("/Containers/")
    return render_to_response('Containers_info.html',locals())
get_Cpuinfo = {}
get_Meninfo = {}
@csrf_exempt
def Containers_Cpu_Get(request):
    global get_Cpuinfo
    CPU = Cpu_mem.objects.filter(Cid__contains=request.GET['Cid'])
    for a in range(0, len(CPU)):
        get = Cpu_mem.objects.filter(Time_float__contains=CPU[a].Time_float)
        get_Cpuinfo = {'Cpu':float(get[0].Cpu)}
    return HttpResponse(json.dumps(get_Cpuinfo),content_type='application/json')
def Containers_Men_Get(request):
    global get_Meninfo
    MEN = Cpu_mem.objects.filter(Cid__contains=request.GET['Cid'])
    for a in range(0, len(MEN)):
        get = Cpu_mem.objects.filter(Time_float__contains=MEN[a].Time_float)
        get_Meninfo = {'Men':float(get[0].Men)}
    return HttpResponse(json.dumps(get_Meninfo),content_type='application/json')
def Containers_Rx(request):
    global get_Meninfo
    Rx = Cpu_mem.objects.filter(Cid__contains=request.GET['Cid'])
    for a in range(0, len(Rx)):
        get = Cpu_mem.objects.filter(Time_float__contains=Rx[a].Time_float)
        get_Meninfo = {'Rx':float(get[0].Rx)}
    return HttpResponse(json.dumps(get_Meninfo),content_type='application/json')
def Containers_Tx(request):
    global get_Meninfo
    Tx = Cpu_mem.objects.filter(Cid__contains=request.GET['Cid'])
    for a in range(0, len(Tx)):
        get = Cpu_mem.objects.filter(Time_float__contains=Tx[a].Time_float)
        get_Meninfo = {'Tx':float(get[0].Tx)}
    return HttpResponse(json.dumps(get_Meninfo),content_type='application/json')
@csrf_exempt
def Containers_Del(request,Del_Ip):
    load = {'force': 'true'}
    All = str(Del_Ip)
    r = requests.delete(All,params=load)
    return HttpResponse()
def Containers_Create(request):
    Ip_get = ip.objects.filter(Ip__contains='http')
    if (Ip_get == ''):
        return render_to_response('Containers_Create.html')
    return render_to_response('Containers_Create.html',locals())
@csrf_exempt
def ImageCreate(request):
    HostIP = str(request.POST['Host'])
    Image = str(request.POST['ImageName'])
    ImageName = Image.split(":")[0]
    if(len(Image.split(":"))==2):
        ImageTag = Image.split(":")[1]
    else:
        ImageTag = "latest"
    url = HostIP + ":2375/images/create?fromImage=" + ImageName + "&tag=" +ImageTag
    r = requests.post(url)
    if(r.status_code == requests.codes.ok):
        response = JsonResponse({"success":"OK"})
        response.status_code = 200
        return response
    else:
        if(r.status_code == 404):
            response = JsonResponse({"error": "repository does not exist or no read access"})
            response.status_code = 404
            return response
        else:
            response = JsonResponse({"error": ImageName})
            response.status_code = 500
            return response
@csrf_exempt
def Create(request):
    hostIP = str(request.POST['host'])
    Image = str(request.POST['ImageName'])
    Name = str(request.POST['Name'])
    HostPort = request.POST.getlist('HostPort')
    ContainersPort =request.POST.getlist('ContainersPort')
    TcpUdp =request.POST.getlist('TcpUdp')
    ExposedPorts = {}
    PortBindings = {}
    for r in range(len(HostPort)):
        ExposedPorts[ContainersPort[r]+'/'+TcpUdp[r]] = {}
    for r in range(len(HostPort)):
        PortBindings[ContainersPort[r]+'/'+TcpUdp[r]] = [
            {
                "HostPort" : HostPort[r]
            }
        ]
    if(str(request.POST['PublishAllPorts'])=="true"):
        PublishAllPorts = True
    elif(str(request.POST['PublishAllPorts'])=="false"):
        PublishAllPorts = False
    ImageName = Image.split(":")[0]
    if (len(Image.split(":")) == 2):
        ImageTag = Image.split(":")[1]
    else:
        ImageTag = "latest"
    load = {
        'Image':ImageName+":"+ImageTag,
        "HostConfig":{
            'PublishAllPorts': PublishAllPorts,
            "PortBindings": PortBindings
        },
        "ExposedPorts": ExposedPorts
    }
    url = hostIP + ":2375/containers/create?name="+Name
    r = requests.post(url,json=load)
    doc = json.loads(r.text)
    if (r.status_code == 201):
        response = JsonResponse({"success": "OK","Id":doc['Id']})
        response.status_code = 200
        return response
    else:
        if (r.status_code == 404):
            response = JsonResponse({"error": "repository does not exist or no read access"})
            response.status_code = 404
            return response
        elif(r.status_code == 400):
            response = JsonResponse({"error": hostIP})
            response.status_code = 400
            return response
        elif(r.status_code == 409):
            response = JsonResponse({"error": hostIP})
            response.status_code = 409
            return response
        elif(r.status_code == 500):
            response = JsonResponse({"error": hostIP})
            response.status_code = 500
            return response