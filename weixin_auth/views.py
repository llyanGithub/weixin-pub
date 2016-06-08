#! /bin/python
# coding=utf-8

from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse

from django.views.decorators.csrf import csrf_exempt

import weixin_app

@csrf_exempt
def weixin_index(request):
    return HttpResponse('<h1>Wechat Index by llyan<h1>')


@csrf_exempt
def weixin_main(request):
    print "weixin_main"
    
    if request.method == 'GET':
        return weixin_app.process_GET(request)

    elif request.method == 'POST':
        return weixin_app.process_POST(request)

    return HttpResponse('error')
