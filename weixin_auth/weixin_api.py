#! /bin/python
# coding=utf-8

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

class Weixin_get_msg:
    def __init__(self):
        return

    def get_msgType(self, root):
        return root.find('MsgType').text

    def get_textMsgContent(self, root):
        return root.find('Content').text

    def get_eventKey(self, root):
        return root.find("EventKey").text

    def get_subEvent(self, root):
        return root.find('Event').text

    def get_echostr(self, request):
        return request.GET.get('echostr', 'error')

class Weixin_send_msg:
    def __init__(self):
        return

    def build_textMsg_xml(self, root, msg=''):
        self.FromUserName = root.find('FromUserName').text
        self.ToUserName = root.find('ToUserName').text
        if msg == '':
            msg = Weixin_get_msg().get_textMsgContent(root)

        return weixin_data.xmlTextMsg % (self.FromUserName, self.ToUserName, str(int(time.time())), msg)

    def build_img_xml(self, root, imgId):
        self.FromUserName = root.find('FromUserName').text
        self.ToUserName = root.find('ToUserName').text

        return weixin_data.xmlImgMsg % (self.FromUserName, self.ToUserName, str(int(time.time())), imgId)

    def build_article_xml(self, root, articles):
        self.ArticleCount = len(articles)

        self.FromUserName = root.find('FromUserName').text
        self.ToUserName = root.find('ToUserName').text

        self.articleArray = [weixin_data.xmlArticleItem % (self.article['Title'], self.article['Description'], self.article['PicUrl'], self.article['Url']) for self.article in articles]

        return weixin_data.xmlArticle % (self.FromUserName, self.ToUserName, str(int(time.time())), self.ArticleCount, ''.join(self.articleArray))



class Weixin_manage_users:
    def __init__(self):
        return

    def get_user_list(self):
        self.token = get_access_token()
        self.request = weixin_data.https_api['get_user_list'] % token
        self.content = urllib2.urlopen(request).read()

        self.result = json.loads(content)
        return self.result 

    def get_user_info(self, openid):
        self.token = get_access_token()
        self.request = weixin_data.https_api['get_user_info'] % (token, openid)
        self.content = urllib2.urlopen(request).read()

        self.result = json.loads(self.content)
        return self.result 

    def batch_get_user_info(self):
        self.token = get_access_token()
        self.request = weixin_data.https_api['batchget_user_info'] % token
        self.content = urllib2.urlopen(request).read()

        self.result = json.loads(self.content)
        return self.result 


class Weixin_ui:
    def __init__(self):
        return

    def create_menu(self):
        self.https = weixin_data.https_api['create_menu']
        self.token = get_access_token()

        self.request = urllib2.Request(https % (self.token), json.dumps(weixin_data.menu))
        self.result = urllib2.urlopen(self.request).read()

        self.result = json.loads(self.result)

        #print result
        return self.result['errcode']

class Weixin_material:
    def __init__(self):
        return

# fielType must one of them : 'image', 'voice', 'video', thumb'
    def upload_tmp_material(self, fileName, fileType):
        register_openers()
        self.token = get_access_token()

        self.https = weixin_data.https_api['upload_tmp_material']

        self.datagen, self.headers = multipart_encode({fileType:open(fileName, "rb")})
        self.request = urllib2.Request(https % (self.token, fileType), self.datagen, self.headers)

        self.result = urllib2.urlopen(self.request).read()
        self.result = json.dumps(self.result)

        return self.result


    def get_material_count(self):
        self.https = weixin_data.https_api['get_materialcount']

        self.token = get_access_token()

        self.result = urllib2.urlopen(https % self.token).read()

        self.result = json.dumps(self.result)
        #print result
        return self.result['errcode']

    def get_material_list(self, arg):
        self.https = weixin_data.https_api['batchget_material'] 

        self.token = get_access_token()
        self.request = urllib2.Request(self.https % (self.token), json.dumps(arg))

        self.result = urllib2.urlopen(self.request).read()

        self.result = json.loads(self.result)

        #print result
        return self.result['errcode']

if __name__ == '__main__':
    print 'testing weixin_api starting...'
