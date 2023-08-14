# -*- coding:utf-8 -*-
import requests

if __name__ == "__main__":
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.66 Safari/537.36',
    }

    url = 'http://xuexiao.51sxue.com/slist/?t=2&areaCodeS=31&page=2'
    # param = {
    #     't' : '2',
    #     'areaCodeS' : '31',
    #     'page' : '2',
    # }
    res =requests.get(url=url,headers=headers)
    res.encoding = res.apparent_encoding
    page_text = res.text
    with open('./pages.html','w',encoding='utf-8') as fp:
        fp.write(page_text)
    print('over!')