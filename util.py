# coding: utf-8

import requests


def getPage(url):
    res = requests.get(url)
    res.encoding = res.apparent_encoding
    html = res.text
    # print(res.encoding)
    return html
