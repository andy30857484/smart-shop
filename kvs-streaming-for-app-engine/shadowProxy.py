import requests
import json
import ast
import shadowProxyConfig

def get(device):#get shadow
    url = 'https://'+shadowProxyConfig.endpoint+':8443/things/'+ device +'/shadow?name=' + shadowProxyConfig.shadowName
    shadowresponse = requests.get(url, cert=(shadowProxyConfig.certificate, shadowProxyConfig.private_key))
    
    begin=str(shadowresponse.text).find('playbackSecond')
    end= str(shadowresponse.text).find('rtsp')
    second= str(shadowresponse.text)[begin+len('playblackSecond:'):end-2]
    second='10'
    return int(second)
