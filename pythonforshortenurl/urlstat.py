import requests
from yourls import YOURLSClient

urlshort = YOURLSClient('https://url.ray361.com/yourls-api.php', signature='25a586e44b')
keyfile = open('urlkey.txt')
kkk = keyfile.readlines()
clickresult = open('clicks.txt', 'a+')
for u in kkk:
    u = u.strip('\n')
    ccc = urlshort.url_stats(u)
    c = ccc.clicks
    print (c)
    clickresult.write(u)
    clickresult.write(',')
    clickresult.write(str(c))
    clickresult.write('\n')
keyfile.close