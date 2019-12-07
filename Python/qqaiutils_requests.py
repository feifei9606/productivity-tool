#!/usr/bin/env python
# coding: utf-8

import hashlib
import base64
import json
import time
import requests
import urllib.parse
url_prefix = 'https://api.ai.qq.com/fcgi-bin/'

def setParams(array, key, value):
    array[key] = value
def genSignString(parser):
    uri_str = ''
    for key in sorted(parser.keys()):
        if key == 'app_key':
            continue
        uri_str += "%s=%s&" % (key, urllib.parse.quote(str(parser[key]), safe = ''))
    sign_str = uri_str + 'app_key=' + parser['app_key']
    
    hl = hashlib.md5()
    hl.update(sign_str.encode(encoding='utf-8'))
    return hl.hexdigest().upper()

class AiPlat(object):
    def __init__(self, app_id, app_key):
        self.app_id = app_id
        self.app_key = app_key
        self.data = {}

    def invoke(self, params):
        try:
            rsp = requests.post(self.url,data=self.data)
            dict_rsp = rsp.json()
            return dict_rsp
        except requests.exceptions.HTTPError as e:
            dict_error = {}
            if hasattr(e.response, "code"):
                dict_error = {}
                dict_error['ret'] = -1
                dict_error['httpcode'] = e.response.status_code
                dict_error['msg'] = "sdk http post err"
                return dict_error
            if hasattr(e.response,"reason"):
                dict_error['msg'] = 'sdk http post err'
                dict_error['httpcode'] = -1
                dict_error['ret'] = -1
                return dict_error
        else:
            dict_error = {}
            dict_error['ret'] = -1
            dict_error['httpcode'] = -1
            dict_error['msg'] = "system error"
            return dict_error
        
    def getOcrGeneralocr(self, image):
        self.url = url_prefix + 'ocr/ocr_generalocr'
        setParams(self.data, 'app_id', self.app_id)
        setParams(self.data, 'app_key', self.app_key)
        setParams(self.data, 'time_stamp', int(time.time()))
        setParams(self.data, 'nonce_str', int(time.time()))
        image_data = base64.b64encode(image).decode('ascii')
        setParams(self.data, 'image', image_data)
        sign_str = genSignString(self.data)
        setParams(self.data, 'sign', sign_str)
        return self.invoke(self.data)

    def getNlpTextTrans(self, text, type):
        self.url = url_prefix + 'nlp/nlp_texttrans'
        setParams(self.data, 'app_id', self.app_id)
        setParams(self.data, 'app_key', self.app_key)
        setParams(self.data, 'time_stamp', int(time.time()))
        setParams(self.data, 'nonce_str', int(time.time()))
        setParams(self.data, 'text', text)
        setParams(self.data, 'type', type)
        sign_str = genSignString(self.data)
        setParams(self.data, 'sign', sign_str)
        return self.invoke(self.data)

    def getAaiWxAsrs(self, chunk, speech_id, end_flag, format_id, rate, bits, seq, chunk_len, cont_res):
        self.url = url_prefix + 'aai/aai_wxasrs'
        setParams(self.data, 'app_id', self.app_id)
        setParams(self.data, 'app_key', self.app_key)
        setParams(self.data, 'time_stamp', int(time.time()))
        setParams(self.data, 'nonce_str', int(time.time()))
        speech_chunk = base64.b64encode(chunk)
        setParams(self.data, 'speech_chunk', speech_chunk)
        setParams(self.data, 'speech_id', speech_id)
        setParams(self.data, 'end', end_flag)

