#! /bin/python
#coding=utf-8

from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse
import hashlib

from django.views.decorators.csrf import csrf_exempt

import os
import re
import time
import xml.etree.ElementTree as ET

import weixin_menu

#Just for weixin test Account
#token = "llyan"

#For weixin Account
token = "lakjd342432akfakfja"

def weixin_process_click_event(root):
    key = root.find("EventKey").text
    for menu in weixin_menu.menu['button']:
        if key in menu.values():
            name = menu.get('name', 'invalid key')
            if name == 'images':
                return weixin_send_imgMsg(root, 'mpg8h8TZ6-vBKebGVkq_I5tlJ-s_VJqKF9za9IhG_OQm7YTiTSTJKk-bOxvw9gC7')
            elif name == 'articles':
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
                return weixin_send_articles(root, articles) 
            return weixin_send_textMsg(root, False, name)

    return weixin_send_textMsg(root, False, key)
    

def weixin_process_event(root):
    Event = root.find('Event').text
    if Event == 'CLICK':
        print "event CLICK"
        #return weixin_send_imgMsg(root, 'mpg8h8TZ6-vBKebGVkq_I5tlJ-s_VJqKF9za9IhG_OQm7YTiTSTJKk-bOxvw9gC7')
        return weixin_process_click_event(root)
    elif Event == 'unsubscribe':
        print 'unsubscribe'
        return weixin_send_textMsg(root, False, '')
    elif Event == 'subscribe':
        print 'subscribe'
        return weixin_send_textMsg(root, False, 
                r"""你好，欢迎关注我的微信公众号
        1). 输入news:查看图文信息
        2). 输入其他字符：原样返回"""
                )
    return

def weixin_send_articles(root, articles):
    xmlArticle = """<xml>
        <ToUserName><![CDATA[%s]]></ToUserName>
        <FromUserName><![CDATA[%s]]></FromUserName>
        <CreateTime>%s</CreateTime>
        <MsgType><![CDATA[news]]></MsgType>
        <ArticleCount>%s</ArticleCount>
        <Articles>%s</Articles>
        </xml>"""
    xmlArticleItem = """
        <item>
        <Title><![CDATA[%s]]></Title>
        <Description><![CDATA[%s]]></Description>
        <PicUrl><![CDATA[%s]]></PicUrl>
        <Url><![CDATA[%s]]></Url>
        </item>"""

    ArticleCount = len(articles)

    FromUserName = root.find('FromUserName').text
    ToUserName = root.find('ToUserName').text

    articleArray = [xmlArticleItem % (article['Title'], article['Description'], article['PicUrl'], article['Url']) for article in articles]

    return HttpResponse(xmlArticle % (FromUserName, ToUserName, str(int(time.time())), ArticleCount, ''.join(articleArray)))

def weixin_send_imgMsg(root, imgId):
    xmlImgMsg = """<xml>
    <ToUserName><![CDATA[%s]]></ToUserName>
    <FromUserName><![CDATA[%s]]></FromUserName>
    <CreateTime>%s</CreateTime>
    <MsgType><![CDATA[image]]></MsgType>
    <Image>
    <MediaId><![CDATA[%s]]></MediaId>
    </Image>
    </xml>"""

    FromUserName = root.find('FromUserName').text
    ToUserName = root.find('ToUserName').text

    return HttpResponse(xmlImgMsg % (FromUserName, ToUserName, str(int(time.time())), imgId))

def weixin_send_textMsg(root, loop = True, msg=''):
    xmlTextMsg = """<xml><ToUserName><![CDATA[%s]]></ToUserName>
    <FromUserName><![CDATA[%s]]></FromUserName>
    <CreateTime>%s</CreateTime>
    <MsgType><![CDATA[%s]]></MsgType>
    <Content><![CDATA[%s]]></Content>
    </xml> """

    FromUserName = root.find('FromUserName').text
    try:
        Content = root.find('Content').text
    except:
        Content = msg
    ToUserName = root.find('ToUserName').text
    CreateTime = root.find('CreateTime').text

    return HttpResponse(xmlTextMsg % (FromUserName, ToUserName, str(int(time.time())), 'text', (Content if loop else msg)))

def weixin_auth(request):
    signature = request.GET.get('signature', 'error')
    timestamp = request.GET.get('timestamp', 'error')
    nonce = request.GET.get('nonce', 'error')

    array = [timestamp, nonce, token]
    array.sort()
    s=''.join(array)

    ret = hashlib.sha1(s).hexdigest()

    if ret == signature:
        print "weixin authentication successful"
        return True
    else:
        print "weixin authentication failed"
        return False

@csrf_exempt
def weixin_index(request):
    return HttpResponse('<h1>Wechat Index by llyan<h1>')

@csrf_exempt
def weixin_main(request):
    print "weixin_main"
    
    if request.method == 'GET':
        if weixin_auth(request):
            echostr = request.GET.get('echostr', 'error')
            return HttpResponse(echostr)
        else:
            return HttpResponse('')

    elif request.method == 'POST':
        if weixin_auth(request):
            root = ET.fromstring(request.body)
            MsgType = root.find('MsgType').text

            if MsgType == 'text':
                msg = root.find('Content').text
                if msg == 'news':
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
                    return weixin_send_articles(root, articles) 
                else:
                    return weixin_send_textMsg(root)
            elif MsgType == 'image':
                print "Receive image"
            elif MsgType == 'voice':
                print "Receive voice"
            elif MsgType == 'video':
                print "Receive video"
            elif MsgType == 'shortvideo':
                print "Receive shortvideo"
            elif MsgType == 'location':
                print "Receive location"
            elif MsgType == 'event':
                print "Receive event"
                return weixin_process_event(root)

    return HttpResponse('error')
