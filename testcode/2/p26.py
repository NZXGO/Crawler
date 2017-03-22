# -*- coding: utf-8 -*-
"""
Created on Mon Mar 20 16:19:55 2017

@author: 小甜甜
"""

from __future__ import print_function, division
import urllib2
import urlparse
import re

def download(url, user_agent='tt', proxy=None, num_retries=2):
    """
    下载某个链接的网页内容
    url，网址
    user_agent，用户代理名，默认为tt
    proxy，代理服务器，翻墙
    num_retries，当服务器端出现错误时，重试下载的次数
    返回：已下载好的网页
    """
    print( 'Downloading:', url )
    headers = {'User-agent': user_agent}
    request = urllib2.Request(url, headers=headers)
    
    opener = urllib2.build_opener()
    if proxy:
        proxy_params = {urlparse.urlparse(url).scheme: proxy}
        opener.add_handler(urllib2.ProxyHandler(proxy_params))
    try:
        html = opener.open(request).read()
    except urllib2.URLError as e:
        print( 'Download error', e.reason )
        html = None
        if num_retries>0:
            if hasattr(e, 'code') and 500 <= e.code <600:
                #recursively retry 5xx HTTP errors
                return download(url, user_agent, proxy, num_retries-1)
    return html

url = 'http://example.webscraping.com/view/United-Kingdom-239'

html = download(url)
#.*?<td\s*class\s*=\s*["\']w2p_fw["\']>(.*?)</td>

print(re.findall('<tr.*?id=\s*"places_area__row".*?>.*?<td\s*class\s*=\s*["\']w2p_fw["\']>(.*?)</td>', html))







