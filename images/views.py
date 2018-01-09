from django.shortcuts import render_to_response
from django.template import RequestContext
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponseRedirect, HttpResponse
import json
import requests
from dashboard.models import ip
from containers.models import Info
from images.models import info,post,SearchInfo
import re
import time

@csrf_exempt
def Images_info(request):
    ALL = str(request)
    b = ":2375/images/json"
    Ip = ALL[7 : ]
    I = "http://" + Ip + b
    r = requests.get(I)
    doc = json.loads(r.text)
    patternID = re.compile(r'sha256:(.*)')
    patternRepoTags = re.compile(r'(.*):(.*)')
    for r in range(0, len(doc)):

        info_db = info.objects.create()
#-----------------------------------------------------------------------
        #info_db.RepoTags = doc[r]['RepoTags']
        RT = doc[r]['RepoTags'][0]
        OT = doc[r]['RepoTags'][0]
        strRT = OT.split(':')
        matchRT = patternRepoTags.match(RT[0])

        IID = doc[r]['Id']

        Time = doc[r]['Created']
        TIME = time.gmtime(Time)

        SIZE = doc[r]['Size']
        S = SIZE/1000/1000
        Resize = str(S)
        Serch = Info.objects.filter(Image__contains=strRT[0])
        Ser_list= list(Serch)
        count = 0
        if(Ser_list == []):
            count = 0
        else:
            count = 1
#-----------------------------------------------------------------------
        info_db.Repository = strRT[0]
        info_db.Tag = strRT[1]
        info_db.ImageId = IID
        info_db.Created = str(TIME[0])+"/"+str(TIME[1])+"/"+str(TIME[2])
        info_db.Size = Resize
        info_db.Ip = Ip
        info_db.count = count
        info_db.save()
    return  HttpResponseRedirect("/Images/")

#-----------------------------------------------------IMAGES-----------------------------------------------------------------
@csrf_exempt
def Images(request):
    Ip_get = ip.objects.filter(Ip__contains='http')
    if(Ip_get==''):
        return render_to_response('Images.html')
    else:
        Info = info.objects.all()
        Info.delete()
        for r in range(0,len(Ip_get)):
            Images_info(Ip_get[r].Ip)
        return render_to_response('Images.html',locals())
#-----------------------------------------------------PULL-----------------------------------------------------------------
@csrf_exempt
def Images_pull(request):

    patternName = re.compile(r'(.+)?:(.*)')
    data = request.POST
    name = str(data['PullName'])
    matchURL = patternName.match(name)
    if(matchURL==None):
        Name = name+":latest"
    else:
        Name = name
    IP = str(data['Pull_IP'])
    url = IP+":2375/images/create?fromImage=" + Name
    requests.post(url)
    return  HttpResponseRedirect("/Images/")
#-----------------------------------------------------REMOVE-----------------------------------------------------------------
@csrf_exempt
def Images_remove(request,Del_Ip):
    load = {'force': 'true'}
    All = str(Del_Ip)
    r = requests.delete(All, params=load)
    return HttpResponse(r)

@csrf_exempt
def Images_search(request):
    data = request.POST
    Name = data["Name"]
    IP = str(data['Search_IP'])
    url = IP+":2375/images/search?term=" + Name
    rq = requests.get(url)

    doc = json.loads(rq.text)

    INFO = SearchInfo.objects.all()
    INFO.delete()
    for i in range(0,10):
        info_db = SearchInfo.objects.create()
        info_db.Stars = str(sorted(doc,key=lambda x:x['star_count'],reverse=True)[i]['star_count'])
        info_db.SearchName = sorted(doc,key=lambda x:x['star_count'],reverse=True)[i]['name']
        info_db.Description = sorted(doc,key=lambda x:x['star_count'],reverse=True)[i]['description']
        info_db.save()
    return render_to_response('Images_search.html',locals())