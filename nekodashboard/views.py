from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response
from django.contrib import auth
from django.views.decorators.csrf import csrf_exempt


@csrf_exempt
def login(request):
    if request.user.is_authenticated():
        return HttpResponseRedirect('/Dashboard/')

    username = request.POST.get('username', '')
    password = request.POST.get('password', '')

    user = auth.authenticate(username=username, password=password)

    if user is not None and user.is_active:
        auth.login(request, user)
        return HttpResponseRedirect('/Dashboard/')
    else:
        return render_to_response('login.html')
@csrf_exempt
def logout(request):
    auth.logout(request)
    return HttpResponseRedirect('/Dashboard/')

