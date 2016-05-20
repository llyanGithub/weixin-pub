#! /bin/bash

#APPID="wx56acb26201686b25"
APPID="wx7f2f982ebe772b4b"
#APPSECRET="ff4c119fa94e21111959af81696e7e69"
APPSECRET='d025ffdfa43e94b80663ac8fec5bdd21'

curl "https://api.weixin.qq.com/cgi-bin/token?grant_type=client_credential&appid=$APPID&secret=$APPSECRET"

