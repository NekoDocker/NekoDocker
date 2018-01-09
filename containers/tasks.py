import time
from celery import Celery
from celery.task import task
from datetime import timedelta
import json
import requests
from containers.models import Info,Cpu_mem
from dashboard.models import info,ip

@task()
def Containers_Cpu(Id):
    Dele = Cpu_mem.objects.filter(Cid__contains=Id)
    Dele.delete()
    b = ":2375/containers/"+str(Id) + "/stats"
    INFO = Info.objects.filter(Cid__contains=Id)
    All = str(INFO[0].Ip)
    IP =  "http://"+All+b
    r = requests.get(IP,{'stream':False})
    doc = json.loads(r.text)
    cpuDelta = float(doc['cpu_stats']['cpu_usage']['total_usage']) - float(doc['precpu_stats']['cpu_usage']['total_usage'])
    systemDelta = float(doc['cpu_stats']['system_cpu_usage']) - float(doc['precpu_stats']['system_cpu_usage'])
    Rx = float(doc['networks']['eth0']['rx_bytes'])
    Tx = float(doc['networks']['eth0']['tx_bytes'])
    Cpu = Cpu_mem.objects.create()
    if (systemDelta > 0.0 or cpuDelta > 0.0):
        cpuPercent = float('%.2f'%((cpuDelta / systemDelta) * float(len(doc['cpu_stats']['cpu_usage']['percpu_usage'])) * 100.0))
        menPercent = float('%.2f'%(float(doc['memory_stats']['usage'])/float(doc['memory_stats']['limit'])*100.0))
        Cpu.Rx = Rx / 1000.0
        Cpu.Tx = Tx / 1000.0
        Cpu.Cpu = cpuPercent
        Cpu.Men = menPercent
    Cpu.Ip = All
    Cpu.Time = time.strftime("%H:%M:%S")
    Cpu.Time_float = time.time()
    Cpu.Cid = Id
    Cpu.save()
@task()
def All_Host():
    Ip = ip.objects.all()
    for r in range(0, len(Ip)):
        All_Host_Containers.delay(Ip[r].Ip)

@task()
def All_Host_Containers(request):
    X = request[7:]
    Id = Info.objects.filter(Ip__contains=X)
    for r in range(0,len(Id)):
        if(Id[r].State == "running"):
            Containers_Cpu.delay(Id[r].Cid)