# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2017-11-20 18:34
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('containers', '0008_auto_20171118_2001'),
    ]

    operations = [
        migrations.AddField(
            model_name='cpu_mem',
            name='Men',
            field=models.CharField(blank=True, max_length=33),
        ),
    ]