#! /bin/python
#coding=utf-8

from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse

from django.views.decorators.csrf import csrf_exempt

import os
import re
import xml.etree.ElementTree as ET

import weixin_api
import weixin_data

articles = [
    {
        'Title':'First Article',
        'Description':'Auth:Linglong Yan',
        'PicUrl':'http://b.hiphotos.baidu.com/image/h%3D200/sign=52b5924e8b5494ee982208191df4e0e1/c2fdfc039245d6887554a155a3c27d1ed31b24e8.jpg',
        'Url':'http://mp.weixin.qq.com/s?__biz=MzAxOTUyMjc4OA==&mid=304671849&idx=1&sn=51e99be067058ed8abe9045026f58406&scene=0&previewkey=ZJn9%2BsWvxFrFogN50HG1tMNS9bJajjJKzz%2F0By7ITJA%3D#wechat_redirect'
    },
    {
        'Title':'Second Article',
        'Description':'Auth:Linglong Yan',
        'PicUrl':'http://b.hiphotos.baidu.com/image/h%3D200/sign=52b5924e8b5494ee982208191df4e0e1/c2fdfc039245d6887554a155a3c27d1ed31b24e8.jpg',
        'Url':'http://mp.weixin.qq.com/s?__biz=MzAxOTUyMjc4OA==&mid=304671849&idx=2&sn=d9680517add6544e84603b9b69427e05&scene=0&previewkey=ZJn9%2BsWvxFrFogN50HG1tMNS9bJajjJKzz%2F0By7ITJA%3D#wechat_redirect'
    },
]

def weixin_process_click_event(root):
    key = weixin_api.get_eventKey(root)
    for menu in weixin_data.menu['button']:
        if key in menu.values():
            name = menu.get('name', 'invalid key')
            if name == 'images':
                return weixin_send_imgMsg(root, 'mpg8h8TZ6-vBKebGVkq_I5tlJ-s_VJqKF9za9IhG_OQm7YTiTSTJKk-bOxvw9gC7')
            elif name == 'articles':
                return weixin_send_articles(root, articles) 
            return weixin_send_textMsg(root, name)

    return weixin_send_textMsg(root, key)
    

def weixin_process_event(root):
    subEvent = weixin_api.get_subEvent(root)
    if subEvent == weixin_data.SUB_EVENT_CLICK:
        #print "event CLICK"
        return weixin_process_click_event(root)

    elif subEvent == weixin_data.SUB_EVENT_UNSUBSCRIBE:
        #print 'unsubscribe'
        return weixin_send_textMsg(root, 'subEvent unsubscribe')

    elif subEvent == weixin_data.SUB_EVENT_SUBSCRIBE:
        #print 'subscribe'
        return weixin_send_textMsg(root, r"""你好，欢迎关注我的微信公众号
        1). 输入news:查看图文信息
        2). 输入其他字符：原样返回"""
        )
    elif subEvent == weixin_data.SUB_EVENT_SCAN:
        return weixin_send_textMsg(root, 'subEvent scan')
    elif subEvent == weixin_data.SUB_EVENT_LOCATION:
        return weixin_send_textMsg(root, 'subEvent location')
    elif subEvent == weixin_data.SUB_EVENT_VIEW:
        return weixin_send_textMsg(root, 'subEvent view')

    return

def weixin_send_articles(root, articles):
    articleMsg = weixin_api.build_article_xml(root, articles)
    return HttpResponse(articleMsg)

def weixin_send_imgMsg(root, imgId):
    imgMsg = weixin_api.build_img_xml(root, imgId)
    return HttpResponse(imgMsg)

def weixin_send_textMsg(root, msg=''):
    textMsg = weixin_api.build_textMsg_xml(root, msg)
    return HttpResponse(textMsg)


@csrf_exempt
def weixin_index(request):
    return HttpResponse('<h1>Wechat Index by llyan<h1>')


@csrf_exempt
def weixin_main(request):
    print "weixin_main"
    
    if request.method == 'GET':
        if weixin_api.auth(request):
            echostr = weixin_api.get_echostr(request)
            return HttpResponse(echostr)
        else:
            return HttpResponse('')

    elif request.method == 'POST':
        if weixin_api.auth(request):
            root = ET.fromstring(request.body)
            MsgType = weixin_api.get_msgType(root)

            if MsgType == weixin_data.MSG_TEXT:
                msg = weixin_api.get_textMsgContent(root)
                if msg == 'news':
                    return weixin_send_articles(root, articles) 
                else:
                    return weixin_send_textMsg(root)
            elif MsgType == weixin_data.MSG_IMAGE:
                print "Receive image"
            elif MsgType == weixin_data.MSG_VOICE:
                print "Receive voice"
            elif MsgType == weixin_data.MSG_VIDEO:
                print "Receive video"
            elif MsgType == weixin_data.MSG_SHORTVIDEO:
                print "Receive shortvideo"
            elif MsgType == weixin_data.MSG_LOCATION:
                print "Receive location"
            elif MsgType == weixin_data.MSG_EVENT:
                print "Receive event"
                return weixin_process_event(root)

    return HttpResponse('error')
