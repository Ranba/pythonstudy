import requests
from yourls import YOURLSClient

urlshort = YOURLSClient('https://url.ray361.com/yourls-api.php', signature='25a586e44b')
originaurl = "https://www.163.com"
mmd5 = "134567890098"
origniamd5url = originaurl + "&mob=" + mmd5
print (origniamd5url)
p = urlshort.shorten(origniamd5url)
print(p.shorturl)