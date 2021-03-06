# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2017-12-06 12:39
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='info',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Repository', models.CharField(blank=True, max_length=100)),
                ('Tag', models.CharField(blank=True, max_length=100)),
                ('ImageId', models.CharField(blank=True, max_length=100)),
                ('Created', models.CharField(blank=True, max_length=40)),
                ('Size', models.CharField(blank=True, max_length=100)),
                ('Ip', models.CharField(blank=True, max_length=40)),
            ],
        ),
        migrations.CreateModel(
            name='post',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Name', models.CharField(blank=True, max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='SearchInfo',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('SearchName', models.CharField(blank=True, max_length=40)),
                ('Stars', models.CharField(blank=True, max_length=40)),
                ('Description', models.CharField(blank=True, max_length=100)),
                ('test', models.CharField(blank=True, max_length=40)),
            ],
        ),
    ]
