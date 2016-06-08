APPID = "wx7f2f982ebe772b4b"
APPSECRET = "d025ffdfa43e94b80663ac8fec5bdd21"
TOKEN = "llyan"

https_api = {
    'access_token': "https://api.weixin.qq.com/cgi-bin/token?grant_type=client_credential&appid=%s&secret=%s",
    'create_menu' : "https://api.weixin.qq.com/cgi-bin/menu/create?access_token=%s",
    'get_materialcount' :"https://api.weixin.qq.com/cgi-bin/material/get_materialcount?access_token=%s",
    'batchget_material' : "https://api.weixin.qq.com/cgi-bin/material/batchget_material?access_token=%s",
    'getcallbackip': "https://api.weixin.qq.com/cgi-bin/getcallbackip?access_token=%s",
    'get_user_list':"https://api.weixin.qq.com/cgi-bin/user/get?access_token=%s&next_openid=",
    'get_user_info':'https://api.weixin.qq.com/cgi-bin/user/info?access_token=%s&openid=%s&lang=zh_CN',
    'batchget_user_info':"https://api.weixin.qq.com/cgi-bin/user/info/batchget?access_token=%s",
    'upload_tmp_material':"https://api.weixin.qq.com/cgi-bin/media/upload?access_token=%s&type=%s",
        }

MSG_TEXT = 'text'
MSG_IMAGE = 'image'
MSG_VOICE = 'voice'
MSG_VIDEO = 'video'
MSG_SHORTVIDEO = 'shortvideo'
MSG_LOCATION= 'location'
MSG_EVENT= 'event'

SUB_EVENT_CLICK = 'CLICK'
SUB_EVENT_UNSUBSCRIBE= 'unsubscribe'
SUB_EVENT_SUBSCRIBE= 'subscribe'
SUB_EVENT_SCAN = 'SCAN'
SUB_EVENT_LOCATION= 'LOCATION'
SUB_EVENT_VIEW = 'VIEW'

xmlTextMsg = """<xml><ToUserName><![CDATA[%s]]></ToUserName>
<FromUserName><![CDATA[%s]]></FromUserName>
<CreateTime>%s</CreateTime>
<MsgType><![CDATA[text]]></MsgType>
<Content><![CDATA[%s]]></Content>
</xml> """

xmlImgMsg = """<xml>
<ToUserName><![CDATA[%s]]></ToUserName>
<FromUserName><![CDATA[%s]]></FromUserName>
<CreateTime>%s</CreateTime>
<MsgType><![CDATA[image]]></MsgType>
<Image>
<MediaId><![CDATA[%s]]></MediaId>
</Image>
</xml>"""

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