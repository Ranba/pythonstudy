# -*- coding: utf-8 -*-
import hashlib
import requests
from yourls import YOURLSClient

def md5(str):
    m = hashlib.md5()
    m.update(str.encode(encoding='UTF-8'))
    return m.hexdigest()

urlshort = YOURLSClient('https://url.ray361.com/yourls-api.php', signature='25a586e44b')
ourl = "https://www.baidu.com/s?ie=utf-8&f=8&rsv_bp=1&rsv_idx=1&tn=baidu&wd=%E6%B5%8B%E8%AF%95"

mobfile = open("pythonforshortenurl\m.txt")
mob = mobfile.readlines()
mobmd5file = open('mmd5.txt','a+')
mobmd5keyfile = open('urlkey.txt','a+')
for a in mob:
    a = a.strip('\n')
    amd5 = md5(a)
    print (amd5)
    omd5url = ourl + "&t=" + amd5
    p = urlshort.shorten(omd5url)
    mobmd5file.write(a)
    mobmd5file.write(',')
    mobmd5file.write(amd5)
    mobmd5file.write(',')
    mobmd5file.write(p.shorturl)
    mobmd5file.write('\n')
    mobmd5keyfile.write(p.keyword)
    mobmd5keyfile.write('\n')
mobfile.close()
mobmd5file.close()

