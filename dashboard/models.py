# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.db import models

class info(models.Model):
    Ip = models.CharField(max_length=33,blank=True)
    Name = models.CharField(max_length=40)
    Architecture = models.CharField(max_length=40)
    ServerVersion = models.CharField(max_length=40)
    NCPU = models.CharField(max_length=40)
    MemTotal = models.CharField(max_length=40)
    Containers = models.CharField(max_length=40)
    ContainersPaused = models.CharField(max_length=40)
    ContainersRunning = models.CharField(max_length=40)
    ContainersStopped = models.CharField(max_length=40)
    Images = models.CharField(max_length=40)
    Images_Size = models.CharField(max_length=40,blank=True)
    OperatingSystem = models.CharField(max_length=40,blank=True)
    Tag = models.CharField(max_length=40,blank=True)
class ip(models.Model):
    Ip = models.CharField(max_length=33)
    Tag = models.CharField(max_length=100,blank=True)