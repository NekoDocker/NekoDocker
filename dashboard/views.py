from django.shortcuts import render_to_response
from django.template import RequestContext
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponseRedirect
import json
import requests

import images
from dashboard.models import info,ip

@csrf_exempt
def Dashboard_ip(request):
    Ip = "http://" + request.POST['IP']
    cre = ip.objects.create()
    cre.Ip = Ip
    cre.Tag = request.POST['tag']
    cre.save()
    return HttpResponseRedirect("/Dashboard/")
@csrf_exempt
def Dashboard_info(request,Tag):
    ALL = str(request)
    b = ":2375/info"
    Ip = ALL[7 : ]
    I = "http://"+Ip+b
    r = requests.get(I)
    doc = json.loads(r.text)
    Image = images.models.info.objects.filter(Ip__contains=Ip)
    Size = 0
    for r in range(0,len(Image)):
        Size += int(Image[r].Size)
    info_db = info.objects.create()
    info_db.Ip = Ip
    info_db.Name = doc['Name']
    info_db.OperatingSystem = doc['OperatingSystem']
    info_db.Architecture = doc['Architecture']
    info_db.ServerVersion = doc['ServerVersion']
    info_db.NCPU = doc['NCPU']
    info_db.MemTotal = int(doc['MemTotal'])
    info_db.Containers = doc['Containers']
    info_db.ContainersPaused = doc['ContainersPaused']
    info_db.ContainersRunning = doc['ContainersRunning']
    info_db.ContainersStopped = doc['ContainersStopped']
    info_db.Images = doc['Images']
    info_db.Tag = Tag
    info_db.Images_Size = Size
    info_db.save()
    return HttpResponseRedirect("/Dashboard/")
def Dashboard(request):
    Ip_get = ip.objects.filter(Ip__contains='http')
    if(Ip_get==''):
        return render_to_response('Dashboard.html')
    else:
        Info = info.objects.all()
        Info.delete()
        for r in range(0,len(Ip_get)) :
            Dashboard_info(Ip_get[r].Ip,Ip_get[r].Tag)
        return render_to_response('Dashboard.html',locals())
def Dashboard_search(request):
    INFO = info.objects.filter(Ip__contains=request.GET['Ip'])
    if(INFO == ''):
        return HttpResponseRedirect("/Dashboard/")
    return render_to_response('Host.html',locals())