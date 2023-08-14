#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2019/8/5 21:13
# @Author  : T.M.
# @File    : tm_爬取公众号历史文章.py
# @Software: PyCharm

import requests
import json
import time
import pdfkit


def get_content_url(index, biz, uin, key):
    print('*' * 20)
    print('正在爬取第{}页'.format(index + 1))

    # url前缀
    url = "https://mp.weixin.qq.com/mp/profile_ext"

    # 请求头
    headers = {
        'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 10_0_1 like Mac OS X) AppleWebKit/602.1.50 '
                      '(KHTML, like Gecko) Mobile/14A403 MicroMessenger/6.5.18 NetType/WIFI Language/zh_CN'
    }

    # 重要参数
    param = {
        'action': 'getmsg',
        '__biz': biz,
        'f': 'json',
        'offset': index * 10,
        'uin': uin,
        'key': key
    }

    # 发送请求，获取响应
    reponse = requests.get(url, params=param, headers=headers)
    reponse_dict = reponse.json()

    # print(reponse_dict)

    next_offset = reponse_dict['next_offset']
    can_msg_continue = reponse_dict['can_msg_continue']

    general_msg_list = reponse_dict['general_msg_list']
    data_list = json.loads(general_msg_list)['list']

    # print(data_list)

    for data in data_list:

        try:
            datetime = data['comm_msg_info']['datetime']
            date = time.strftime('%Y-%m-%d', time.localtime(datetime))

            msg_info = data['app_msg_ext_info']

            # 标题
            title = msg_info['title']

            # 内容的url
            content_url = msg_info['content_url']

            print(title + date + '--' + content_url)

            # 自己定义存储路径（绝对路径）
            pdfkit.from_url(content_url, 'D:/小项目/爬取公众号文章/' + date + title + '.pdf')

            print(title + date + '成功')
            print('-' * 20)

        except:
            print("不是图文消息")

    if can_msg_continue == 1:
        return True
    else:
        print('全部获取完毕')
        return False


if __name__ == '__main__':

    index = 0

    # 这三个参数要换成自己的

    biz = 'MzU4MjM0NTk3OQ=='
    uin = 'MjM1ODQyMTMyNg=='
    key = '57d70e971f4521a8c651cb296bb560b84d8c3cf7466cfe04ab51de3f1b4d3d2e9d477b2fb84cf2c169fb7469b91ede6e76e3e7' \
          '5f14229079d1f6be6a6781da79a7ed98455fe6f3d703b0dcd72870ac6c'

    while 1:

        result = get_content_url(index, biz, uin, key)

        time.sleep(2)
        index += 1

        if result == False:
            break
