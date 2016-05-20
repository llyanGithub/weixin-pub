#! /bin/python
#coding=utf-8
import urllib2
import urllib

import json

from access_token import get_access_token

def weixin_get_material_count():
    https = "https://api.weixin.qq.com/cgi-bin/material/get_materialcount?access_token=%s"

    token = get_access_token()

    result = urllib2.urlopen(https % token).read()

    result = json.dumps(result)
    print result
    return

def weixin_get_material_list(arg):
    https = "https://api.weixin.qq.com/cgi-bin/material/batchget_material?access_token=%s"

    token = get_access_token()
    request = urllib2.Request(https % (token), json.dumps(arg))

    result = urllib2.urlopen(request).read()

    result = json.loads(result)

    print result
    return

if __name__ == '__main__':
    #arg = {
        #"type":"image",
        #"offset":0,
        #"count":20
    #}
    #weixin_get_material_list(arg)
    weixin_get_material_count()
