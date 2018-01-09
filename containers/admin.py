# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from containers.models import Info,Cpu_mem
from django.contrib import admin
from kombu.transport.django import models as kombu_models

# Register your models here.
admin.site.register(Info)
admin.site.register(Cpu_mem)
admin.site.register(kombu_models.Message)