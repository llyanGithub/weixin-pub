#! /bin/python
# coding=utf-8

import hashlib

import urllib2
import urllib
import json
import time
import os

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

class Weixin_device:
    def __init__(self):
        return
    def authorize_device(self, post_data):
        self.https = weixin_data.https_api['authorize_device']
        self.token = get_access_token()

        self.request = urllib2.Request(self.https % (self.token), json.dumps(post_data))
        self.result = urllib2.urlopen(self.request).read()

        self.result = json.loads(self.result)

        #print result
        #return self.result['errcode']
        return self.result

    def get_qrcode(self):
        self.token = get_access_token()
        self.request = weixin_data.https_api['get_qrcode'] % (self.token, weixin_data.PRODUCT_ID)
        self.content = urllib2.urlopen(self.request).read()

        self.result = json.loads(self.content)
        return self.result 



class Weixin_semproxy:
    def __init__(self):
        return
    def semproxy_search(self, post_data):
        self.https = weixin_data.https_api['semproxy_search']
        self.token = get_access_token()

        self.request = urllib2.Request(self.https % (self.token), json.dumps(post_data))
        self.result = urllib2.urlopen(self.request).read()

        self.result = json.loads(self.result)

        #return self.result['errcode']
        return self.result

class Weixin_get_msg:
    def __init__(self):
        return

    def get_msgType(self, root):
        return root.find('MsgType').text

    def get_textMsgContent(self, root):
        return root.find('Content').text

    def get_voiceMsgContent(self, root):
        return root.find('Recognition').text

    def get_imageMsgContent(self, root):
        return {"url":root.find('PicUrl').text, "media_id":root.find('MediaId').text}

    def get_locationMsgContent(self, root):
        return {"Location_X":root.find('Location_X').text, "Location_Y":root.find('Location_Y').text}

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
        self.request = weixin_data.https_api['get_user_list'] % self.token
        self.content = urllib2.urlopen(self.request).read()

        self.result = json.loads(self.content)
        return self.result 

    def get_user_info(self, openid):
        self.token = get_access_token()
        self.request = weixin_data.https_api['get_user_info'] % (self.token, openid)
        self.content = urllib2.urlopen(self.request).read()

        self.result = json.loads(self.content)
        return self.result 

    def batch_get_user_info(self, data):
        self.https = weixin_data.https_api['batchget_user_info']
        self.token = get_access_token()

        self.request = urllib2.Request(self.https % (self.token), json.dumps(data))
        self.result = urllib2.urlopen(self.request).read()

        self.result = json.loads(self.result)

        return self.result
        #self.token = get_access_token()
        #self.request = weixin_data.https_api['batchget_user_info'] % self.token
        #self.content = urllib2.urlopen(self.request).read()

        #self.result = json.loads(self.content)
        #return self.result 


class Weixin_ui:
    def __init__(self):
        return

    def create_menu(self, menu):
        self.https = weixin_data.https_api['create_menu']
        self.token = get_access_token()

        self.request = urllib2.Request(self.https % (self.token), json.dumps(menu))
        self.result = urllib2.urlopen(self.request).read()

        self.result = json.loads(self.result)

        #print result
        #return self.result['errcode']
        return self.result
    def get_menu(self):
        self.https = weixin_data.https_api['get_menu']

        self.token = get_access_token()

        self.result = urllib2.urlopen(self.https % self.token).read()

        self.result = json.dumps(self.result)
        #print result
        #return self.result['errcode']
        return self.result
    def del_menu(self):
        self.https = weixin_data.https_api['del_menu']

        self.token = get_access_token()

        self.result = urllib2.urlopen(self.https % self.token).read()

        self.result = json.dumps(self.result)
        #print result
        #return self.result['errcode']
        return self.result

class Weixin_material:
    def __init__(self):
        return

# fielType must one of them : 'image', 'voice', 'video', thumb'
    def upload_tmp_material(self, fileName, fileType):
        register_openers()
        self.token = get_access_token()

        self.https = weixin_data.https_api['upload_tmp_material']

        self.datagen, self.headers = multipart_encode({fileType:open(fileName, "rb")})
        self.request = urllib2.Request(self.https % (self.token, fileType), self.datagen, self.headers)

        self.result = urllib2.urlopen(self.request).read()
        self.result = json.dumps(self.result)

        return self.result

    def upload_material(self, fileName):
        self.token = get_access_token()

        self.https = weixin_data.https_api['upload_material'] % self.token

        self.cmd = 'curl -F media=@%s %s' % (fileName, self.https)
        self.result = os.popen(self.cmd).read()

        self.result = json.dumps(self.result)

        return self.result

    def upload_batch_material(self, fileNames):
        for self.fileName in fileNames:
            self.upload_material(self.fileName)

    def get_material_count(self):
        self.https = weixin_data.https_api['get_materialcount']

        self.token = get_access_token()

        self.result = urllib2.urlopen(self.https % self.token).read()

        self.result = json.loads(self.result)
        #print result
        print type(self.result)
        return self.result

    def get_material_list(self, materialType, materialOffset, materialCnt):
        self.https = weixin_data.https_api['batchget_material'] 

        self.token = get_access_token()
        self.post_data = {
            "type":materialType,
            "offset":materialOffset,
            "count":materialCnt
        }
        self.request = urllib2.Request(self.https % (self.token), json.dumps(self.post_data))

        self.result = urllib2.urlopen(self.request).read()

        self.result = json.loads(self.result)

        #print result
        return self.result

    def del_material(self, media_id):
        self.https = weixin_data.https_api['del_material'] 

        self.token = get_access_token()
        self.post_data = {
            "media_id":media_id
        }
        self.request = urllib2.Request(self.https % (self.token), json.dumps(self.post_data))

        self.result = urllib2.urlopen(self.request).read()

        self.result = json.loads(self.result)

        print self.result, media_id
        return self.result

    def del_all_material(self):
        self.result = []
        for self.material in self.get_all_material():
            for self.item in self.material['item']:
                self.del_material(self.item['media_id'])

    def get_all_material(self):
        self.material = []
        for self.materialType, self.materialCnt in self.get_material_count().items():
            if int(self.materialCnt):
                self.result = self.get_material_list(self.materialType.split('_')[0], 0, int(self.materialCnt))
                self.material.append(self.result)
        return self.material

class Weixin_merchant:
    def __init__(self):
        return
    
    def create(self, post_data):
        https = weixin_data.https_api['merchant_create'] 

        token = get_access_token()
        request = urllib2.Request(https % (token), json.dumps(post_data))

        result = urllib2.urlopen(request).read()

        result = json.loads(result)

        #print result
        return result

    def delete(self, product_id):
        https = weixin_data.https_api['merchant_del'] 

        token = get_access_token()
        request = urllib2.Request(https % (token), json.dumps(post_data))

        result = urllib2.urlopen(request).read()

        result = json.loads(result)

        return result

    def update(self, post_data):
        https = weixin_data.https_api['merchant_update'] 

        token = get_access_token()
        request = urllib2.Request(https % (token), json.dumps(post_data))

        result = urllib2.urlopen(request).read()

        result = json.loads(result)

        #print result
        return result

def test_manage_users():
    manager = Weixin_manage_users()
    print manager.get_user_list() 

    info =  manager.get_user_info('op7Qnt_r_bgoqhezUYjGDt-2WQSo') 
    for key, value in info.items():
        print "%s: %s" % (key, value)

    post_data = {
        "user_list": [
            {
                "openid": "op7Qnt_r_bgoqhezUYjGDt-2WQSo", 
                "lang": "zh-CN"
            }, 
        ]
    }
    info = manager.batch_get_user_info(post_data) 
    userList = info['user_info_list']
    for user_info in userList:
        for key, value in user_info.items():
            print "%s: %s" % (key, value)

def test_ui():
    ui = Weixin_ui()
    print ui.create_menu(weixin_data.menu)
    print ui.get_menu()
    #print ui.del_menu()

def test_semproxy():
    semproxy = Weixin_semproxy()
    appid = weixin_data.APPID
    post_data = {
        "query":r"查一下明天从北京到上海的南航机票",
        "city":r"北京",
        "category": "flight,hotel",
        "appid":"wx7f2f982ebe772b4b",
        "uid":"op7Qnt_r_bgoqhezUYjGDt-2WQSo"
    } 
    print semproxy.semproxy_search(post_data)
    return

def test_device():
    device = Weixin_device()
    #print device.get_qrcode()
    post_data = {
        "device_num":"1",
        "device_list":[
            {
                "id":"dev1",
                "mac":"E84E06317CAD",
                "connect_protocol":"4",
                "auth_key":"1234567890ABCDEF1234567890ABCDEF",
                "close_strategy":"1",
                "conn_strategy":"1",
                "crypt_method":"0",
                "auth_ver":"0",
                "manu_mac_pos":"-1",
                "ser_mac_pos":"-2",
                "ble_simple_protocol": "0"
            }
        ],
        "op_type":"0",
        "product_id": weixin_data.PRODUCT_ID
    }
    print device.authorize_device(post_data)
    return

def test_material():
    material = Weixin_material()
    #print material.upload_tmp_material('weixin_auth/carton.jpg', 'image')
    #print material.upload_material('weixin_auth/carton.jpg')
    #print material.get_material_list('image', 0, 2)
    #print material.get_material_count()
    #print material.get_all_material()
    #material.del_all_material()

    fileNames = ['weixin_auth/carton.jpg', 'weixin_auth/Koala.jpg', 'weixin_auth/Penguins.jpg']
    material.upload_batch_material(fileNames)
    print material.get_material_count()

def test_merchant():
    merchant = Weixin_merchant()
    post_data = {
        "product_base": {
            "category_id": [
                "537074298"
            ],
            "property": [
                {
                    "id": "1075741879",
                    "vid": "1079749967"
                },
                {
                    "id": "1075754127",
                    "vid": "1079795198"
                },
                {
                    "id": "1075777334",
                    "vid": "1079837440"
                }
           ],
            "name": "testaddproduct",
            "sku_info": [
                {
                    "id": "1075741873",
                    "vid": [
                        "1079742386",
                        "1079742363"
                    ]
                }
            ],
            "main_img":
            "http://mmbiz.qpic.cn/mmbiz/3NqDEPaH6Lf8xMvYJwbPQzezy58pcjdq1HGicDia0otrdxADr7XO5gClrGvEgxXJw4feuy7PeZWQKqlyHBO4JvMA/0",
            "img": [
                "http://mmbiz.qpic.cn/mmbiz/3NqDEPaH6Lf8xMvYJwbPQzezy58pcjdq1HGicDia0otrdxADr7XO5gClrGvEgxXJw4feuy7PeZWQKqlyHBO4JvMA/0"
            ],
            "detail": [
                {
                    "text": "test first"
                },
                {
                    "img":
                    "http://mmbiz.qpic.cn/mmbiz/3NqDEPaH6Lf8xMvYJwbPQzezy58pcjdq1HGicDia0otrdxADr7XO5gClrGvEgxXJw4feuy7PeZWQKqlyHBO4JvMA/0"
                },
                {
                    "text": "test again"
                }
            ],
            "buy_limit": 10
            },
        #"sku_list": [
                #{
                    #"sku_id": "1075741873:1079742386",
                    #"price": 30,
                    #"icon_url":
                    #"http://mmbiz.qpic.cn/mmbiz/4whpV1VZl28bJj62XgfHPibY3ORKicN1oJ4CcoIr4BMbfA8LqyyjzOZzqrOGz3f5KWq1QGP3fo6TOTSYD3TBQjuw/0",
                    #"product_code": "testing",
                    #"ori_price": 9000000,
                    #"quantity": 800
                    #},
                #{
                    #"sku_id": "1075741873:1079742363",
                    #"price": 30,
                    #"icon_url":
                    #"http://mmbiz.qpic.cn/mmbiz/4whpV1VZl28bJj62XgfHPibY3ORKicN1oJ4CcoIr4BMbfA8LqyyjzOZzqrOGz3f5KWq1QGP3fo6TOTSYD3TBQjuw/0",
                    #"product_code": "testingtesting",
                    #"ori_price": 9000000,
                    #"quantity": 800
                    #}
        #],
        "attrext": {
                "location": {
                    "country": "中国",
                    "province": "广东省",
                    "city": "广州市",
                    "address": "T.I.T 创意园"
                },
                "isPostFree": 0,
                "isHasReceipt": 1,
                "isUnderGuaranty": 0,
                "isSupportReplace": 0
        },
        "delivery_info": {
                "delivery_type": 0,
                "template_id": 0,
                "express": [
                    {
                        "id": 10000027,
                        "price": 100
                    },
                    {
                        "id": 10000028,
                        "price": 100
                    },
                    {
                        "id": 10000029,
                        "price": 100
                    }
                ]
        }

    }
    print merchant.create(post_data) 
    return

def api_test():
#test_manage_users()
    #test_ui()
    #test_semproxy()
    #test_device()
    #test_material()
    test_merchant()
    return

if __name__ == '__main__':
    print 'testing weixin_api starting...'
    api_test()
