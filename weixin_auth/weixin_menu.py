#! /bin/python
#coding=utf-8
import urllib2
import urllib

import json

from access_token import get_access_token


menu = {
    "button":[
    { 
        "type":"click",
        "name":"images",
        "key":"V1001_TODAY_MUSIC",
        "sub_button":[]
    },
    { 
        "type":"click",
        "name":"articles",
        "key":"V1001_TODAY_VIDEO",
        "sub_button":[]
    },
    ]
}

def weixin_create_menu():
    https = " https://api.weixin.qq.com/cgi-bin/menu/create?access_token=%s"
    #token = access_token.get_access_token()
    token = get_access_token()

    request = urllib2.Request(https % (token), json.dumps(menu))
    result = urllib2.urlopen(request).read()

    result = json.loads(result)

    print result
    return result['errcode']

if __name__ == "__main__":
    weixin_create_menu()
