#! /bin/python
#coding=utf-8
import urllib2
import urllib

import json

#Just For weixin test Account
#APPID="wx7f2f982ebe772b4b"
#APPSECRET='d025ffdfa43e94b80663ac8fec5bdd21'

#for weixin account
APPID = "wx56acb26201686b25"
APPSECRET = "ff4c119fa94e21111959af81696e7e69"

def get_access_token():
    request = "https://api.weixin.qq.com/cgi-bin/token?grant_type=client_credential&appid=%s&secret=%s" % (APPID, APPSECRET)
    content = urllib2.urlopen(request).read()

    result = json.loads(content)
    access_token = result['access_token'] 

    return access_token 
