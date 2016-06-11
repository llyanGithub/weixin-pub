#! /bin/python
# coding=utf-8
import weixin_api

from django.http import HttpResponse

import xml.etree.ElementTree as ET
from weixin_api import Weixin_get_msg, Weixin_send_msg, Weixin_manage_users, Weixin_ui, Weixin_material
import weixin_data

Get_msg = Weixin_get_msg()
Send_msg = Weixin_send_msg()

image_media_id = "e3k9DDlDCiKPvuHLfCIC9YrJ5sse8OM4G6QUpV64NeQa1y1yFyN62Tyd1fr6xdbW"

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
    key = Get_msg.get_eventKey(root)
    for menu in weixin_data.menu['button']:
        if key in menu.values():
            name = menu.get('name', 'invalid key')
            if name == 'images':
                #return weixin_send_imgMsg(root, 'mpg8h8TZ6-vBKebGVkq_I5tlJ-s_VJqKF9za9IhG_OQm7YTiTSTJKk-bOxvw9gC7')
                return weixin_send_imgMsg(root, image_media_id)
            elif name == 'articles':
                return weixin_send_articles(root, articles) 
            return weixin_send_textMsg(root, name)

    return weixin_send_textMsg(root, key)
    

def weixin_process_event(root):
    subEvent = Get_msg.get_subEvent(root)
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
    articleMsg = Send_msg.build_article_xml(root, articles)
    return HttpResponse(articleMsg)

def weixin_send_imgMsg(root, imgId):
    imgMsg = Send_msg.build_img_xml(root, imgId)
    return HttpResponse(imgMsg)

def weixin_send_textMsg(root, msg=''):
    textMsg = Send_msg.build_textMsg_xml(root, msg)
    return HttpResponse(textMsg)


def process_GET(request):
    if weixin_api.auth(request):
        echostr = Get_msg.get_echostr(request)
        return HttpResponse(echostr)
    else:
        return HttpResponse('')

def process_POST(request):
    if weixin_api.auth(request):
        root = ET.fromstring(request.body)
        MsgType = Get_msg.get_msgType(root)

        if MsgType == weixin_data.MSG_TEXT:
            msg = Get_msg.get_textMsgContent(root)
            if msg == 'news':
                return weixin_send_articles(root, articles) 
            else:
                return weixin_send_textMsg(root)
        elif MsgType == weixin_data.MSG_IMAGE:
            print "Receive image"
            imageMsgContent =  Get_msg.get_imageMsgContent(root)
            print imageMsgContent  
            return weixin_send_textMsg(root, r"你发送了一张图片 media_id:%s" % imageMsgContent['media_id'])
        elif MsgType == weixin_data.MSG_VOICE:
            print "Receive voice"
            voiceContent = Get_msg.get_voiceMsgContent(root)
            print "voice: %s" % voiceContent
            return weixin_send_textMsg(root, (r"你说的是: %s" % voiceContent.encode('utf8')))
        elif MsgType == weixin_data.MSG_VIDEO:
            print "Receive video"
        elif MsgType == weixin_data.MSG_SHORTVIDEO:
            print "Receive shortvideo"
        elif MsgType == weixin_data.MSG_LOCATION:
            print "Receive location"
            locationContent = Get_msg.get_locationMsgContent(root)
            return weixin_send_textMsg(root, r"您的位置是, 经度:%s 纬度:%s" % (locationContent['Location_Y'], locationContent['Location_X']))
        elif MsgType == weixin_data.MSG_EVENT:
            print "Receive event"
            return weixin_process_event(root)
    return
