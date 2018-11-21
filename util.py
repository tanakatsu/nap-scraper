# coding: utf-8

import requests


def getPage(url):
    res = requests.get(url)
    # res.encoding = res.apparent_encoding
    res.encoding = 'utf-8'
    html = res.text
    return html
