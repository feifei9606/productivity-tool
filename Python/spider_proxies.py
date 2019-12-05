#!/usr/bin/env python
# coding: utf-8

import requests

## get proxy from proxy pool
def getProxy():
    url = "http://127.0.0.1:5010/get/"
    proxy = requests.get(url,timeout=2).json()["proxy"]
    return proxy

## when proxy does not work, delete proxy
def deleteProxy(proxy):
    url = "http://127.0.0.1:5010/delete?proxy=" + proxy
    deleterequests = requests.get(url,timeout=3)
    return 

## test proxy connectivity
def testProxy(proxy):
    proxy_dict = {"http" : "http://" + proxy, "https" : "https://" + proxy}
    try:
        a = requests.get("https://www.baidu.com",proxies=proxy_dict,timeout=2)
        if a.status_code == 200:
            return True
    except:
        pass
    return False

## return avaliable proxy
def returnProxy():
    proxy = getProxy()
    flag = testProxy(proxy)
    while not flag:
        try:
            deleteProxy(proxy)
            proxy = getProxy()
            flag = testProxy(proxy)
        except:
            continue
    return proxy 

## usage
proxy = returnProxy()
## 159.89.16.64:3128