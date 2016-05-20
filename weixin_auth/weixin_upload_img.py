#! /bin/python
#coding=utf-8
import urllib2
import urllib

import json

from access_token import get_access_token
from poster.encode import multipart_encode
from poster.streaminghttp import register_openers

def weixin_upload_temp_img():
    register_openers()
    https = "https://api.weixin.qq.com/cgi-bin/media/upload?access_token=%s&type=%s"
    token = get_access_token()

    datagen, headers = multipart_encode({"image":open("carton.jpg", "rb")})
    request = urllib2.Request(https % (token, 'image'), datagen, headers)

    result = urllib2.urlopen(request).read()

    print result

def weixin_get_temp_img():
    https = "https://api.weixin.qq.com/cgi-bin/media/get?access_token=%s&media_id=%s"
    token = get_access_token()

    return

if __name__ == "__main__":
    weixin_upload_temp_img()
