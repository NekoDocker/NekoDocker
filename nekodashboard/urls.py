"""test_01 URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import *
from django.contrib import admin
from dashboard.views import Dashboard_info,Dashboard_ip,Dashboard,Dashboard_search
from containers.views import Containers,Containers_search,Containers_Cpu_Get,Containers_Men_Get,Containers_Del,Containers_Rx,Containers_Tx,Containers_Create,ImageCreate,Create
from images.views import Images, Images_pull, Images_remove, Images_search
from views import login,logout


urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^Dashboard/$',Dashboard),
    url(r'^info/$',Dashboard_info),
    url(r'^new_ip/$',Dashboard_ip),
    url(r'^Containers/$',Containers),
    url(r'^Host/$',Dashboard_search),
    url(r'^Containers_search/$',Containers_search),
    url(r'^Containers_create/$', Containers_Create),
    url(r'^Containers_cpu/$', Containers_Cpu_Get),
    url(r'^Containers_men/$', Containers_Men_Get),
    url(r'^Containers_rx/$', Containers_Rx),
    url(r'^Containers_tx/$', Containers_Tx),
    url(r'^Containers_del/(.+)/$', Containers_Del),
    url(r'^Images/$',Images),
    url(r'Images_pull/$',Images_pull),
    url(r'Images_remove/(.+)$',Images_remove),
    url(r'^Images_search/$',Images_search),
    url(r'login', login),
    url(r'logout', logout),
    url(r'ImageCreate/$',ImageCreate),
    url(r'Create/$',Create),
]
