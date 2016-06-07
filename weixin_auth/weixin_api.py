#! /bin/python
#coding=utf-8

import hashlib

import urllib2
import urllib
import json
import time

import weixin_data

from poster.encode import multipart_encode
from poster.streaminghttp import register_openers

def get_access_token():
    request = weixin_data.https_api['access_token'] % (weixin_data.APPID, weixin_data.APPSECRET)
    content = urllib2.urlopen(request).read()

    result = json.loads(content)
    access_token = result['access_token'] 

    return access_token 

def get_callback_ip():
    token = get_access_token()
    request = weixin_data.https_api['getcallbackip'] % token
    content = urllib2.urlopen(request).read()

    result = json.loads(content)
    ip_list = result['ip_list'] 
    return ip_list 

def get_user_list():
    token = get_access_token()
    request = weixin_data.https_api['get_user_list'] % token
    content = urllib2.urlopen(request).read()

    result = json.loads(content)
    return result 

def get_user_info(openid):
    token = get_access_token()
    request = weixin_data.https_api['get_user_info'] % (token, openid)
    content = urllib2.urlopen(request).read()

    result = json.loads(content)
    return result 

def batch_get_user_info():
    token = get_access_token()
    request = weixin_data.https_api['batchget_user_info'] % token
    content = urllib2.urlopen(request).read()

    result = json.loads(content)
    return result 


def auth(request):
    signature = request.GET.get('signature', 'error')
    timestamp = request.GET.get('timestamp', 'error')
    nonce = request.GET.get('nonce', 'error')

    array = [timestamp, nonce, weixin_data.TOKEN]
    array.sort()
    s=''.join(array)

    ret = hashlib.sha1(s).hexdigest()

    if ret == signature:
        #print "weixin authentication successful"
        return True
    else:
        #print "weixin authentication failed"
        return False


def create_menu():
    https = weixin_data.https_api['create_menu']
    token = get_access_token()

    request = urllib2.Request(https % (token), json.dumps(weixin_data.menu))
    result = urllib2.urlopen(request).read()

    result = json.loads(result)

    #print result
    return result['errcode']

# fielType must one of them : 'image', 'voice', 'video', thumb'
def upload_tmp_material(fileName, fileType):
    register_openers()
    token = get_access_token()

    https = weixin_data.https_api['upload_tmp_material']

    datagen, headers = multipart_encode({fileType:open(fileName, "rb")})
    request = urllib2.Request(https % (token, fileType), datagen, headers)

    result = urllib2.urlopen(request).read()
    result = json.dumps(result)

    return result


def get_material_count():
    https = weixin_data.https_api['get_materialcount']

    token = get_access_token()

    result = urllib2.urlopen(https % token).read()

    result = json.dumps(result)
    #print result
    return result['errcode']

def get_material_list(arg):
    https = weixin_data.https_api['batchget_material'] 

    token = get_access_token()
    request = urllib2.Request(https % (token), json.dumps(arg))

    result = urllib2.urlopen(request).read()

    result = json.loads(result)

    #print result
    return result['errcode']

def build_textMsg_xml(root, msg=''):
    FromUserName = root.find('FromUserName').text
    ToUserName = root.find('ToUserName').text
    if msg == '':
        msg = get_textMsgContent(root)

    return weixin_data.xmlTextMsg % (FromUserName, ToUserName, str(int(time.time())), msg)

def build_img_xml(root, imgId):
    FromUserName = root.find('FromUserName').text
    ToUserName = root.find('ToUserName').text

    return weixin_data.xmlImgMsg % (FromUserName, ToUserName, str(int(time.time())), imgId)

def build_article_xml(root, articles):
    ArticleCount = len(articles)

    FromUserName = root.find('FromUserName').text
    ToUserName = root.find('ToUserName').text

    articleArray = [weixin_data.xmlArticleItem % (article['Title'], article['Description'], article['PicUrl'], article['Url']) for article in articles]

    return weixin_data.xmlArticle % (FromUserName, ToUserName, str(int(time.time())), ArticleCount, ''.join(articleArray))

def get_msgType(root):
    return root.find('MsgType').text

def get_textMsgContent(root):
    return root.find('Content').text

def get_eventKey(root):
    return root.find("EventKey").text

def get_subEvent(root):
    return root.find('Event').text

def get_echostr(request):
    return request.GET.get('echostr', 'error')

