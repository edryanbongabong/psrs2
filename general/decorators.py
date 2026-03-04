from django.http import HttpResponse
from django.shortcuts import  render, redirect
from django.http import Http404
from django.contrib.auth import authenticate

def allowed_users(allowed_groups=[]):
    def decorator(view_func):
        def wrapper_func(request, *args, **kwargs):
            group = None
            if request.user.groups.exists():
                group = request.user.groups.all()[0].name
            if group in allowed_groups:
                return view_func(request, *args, **kwargs)
            else:
                print('error')
                raise Http404("This page does not exist.")
        return wrapper_func
    return decorator