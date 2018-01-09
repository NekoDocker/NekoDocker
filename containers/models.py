# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

class Info(models.Model):
    Cid = models.CharField(max_length=100)
    Name = models.CharField(max_length=100,blank=True)
    State = models.CharField(max_length=40)
    Image = models.CharField(max_length=100)
    Command = models.CharField(max_length=100,blank=True)
    PrivatePort = models.CharField(max_length=20,blank=True)
    PublicPort = models.CharField(max_length=20, blank=True)
    Type = models.CharField(max_length=5, blank=True)
    Ip = models.CharField(max_length=33)
class Cpu_mem(models.Model):
    Ip = models.CharField(max_length=33, blank=True)
    Cid = models.CharField(max_length=100, blank=True)
    Time = models.CharField(max_length=100, blank=True)
    Time_float = models.CharField(max_length=100, blank=True)
    Cpu = models.CharField(max_length=40, blank=True)
    Men = models.CharField(max_length=33, blank=True)
    Rx = models.CharField(max_length=33, blank=True)
    Tx = models.CharField(max_length=33, blank=True)