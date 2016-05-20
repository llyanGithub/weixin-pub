#! /bin/python
#coding=utf-8
import urllib2
import urllib

import json

#APPID="wx56acb26201686b25"
APPID="wx7f2f982ebe772b4b"
#APPSECRET="ff4c119fa94e21111959af81696e7e69"
APPSECRET='d025ffdfa43e94b80663ac8fec5bdd21'

request = "https://api.weixin.qq.com/cgi-bin/token?grant_type=client_credential&appid=%s&secret=%s" % (APPID, APPSECRET)

https = " https://api.weixin.qq.com/cgi-bin/menu/create?access_token=%s"
content = urllib2.urlopen(request).read()

result = json.loads(content)

access_token = result['access_token'] 
expires_in = result['expires_in'] 

data = urllib2.urlopen('https://api.weixin.qq.com/cgi-bin/menu/get?access_token=%s' % access_token).read()

print access_token
data = json.loads(data)
print type(data)

data = {
    "button":[
    { 
        "type":"click",
        "name":"songs",
        "key":"V1001_TODAY_MUSIC",
        "sub_button":[]
    },
    { 
        "type":"click",
        "name":"video",
        "key":"V1001_TODAY_VIDEO",
        "sub_button":[]
    },
    #{ 
        #"type":"click",
        #"name":"video",
        #"key":"V1001_TODAY_VIDEO"
    #},
    #{
        #"name":"menu",
        #"sub_button":[
        #{  
            #"type":"view",
            #"name":"search",
            #"url":"http://www.soso.com/"
        #},
        #{
            #"type":"view",
            #"name":"video",
            #"url":"http://v.qq.com/"
        #},
        #{
            #"type":"click",
            #"name":"like me",
            #"key":"V1001_GOOD"
        #}]
    #}
    ]
}

httpsRequest = urllib2.Request(https % (access_token), json.dumps(data))

print urllib2.urlopen(httpsRequest).read()
