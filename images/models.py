# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

class info(models.Model):
    Repository = models.CharField(max_length=100,blank=True)
    Tag = models.CharField(max_length=100,blank=True)
    ImageId = models.CharField(max_length=100,blank=True)
    Created = models.CharField(max_length=40,blank=True)
    Size = models.CharField(max_length=100,blank=True)
    Ip = models.CharField(max_length=40,blank=True)
    count = models.CharField(max_length=3, blank=True)

class post(models.Model):
    Name = models.CharField(max_length=100,blank = True)

class SearchInfo(models.Model):
    SearchName = models.CharField(max_length=40, blank=True)
    Stars = models.CharField(max_length=40, blank=True)
    Description = models.CharField(max_length=100, blank=True)
    test = models.CharField(max_length=40, blank=True)