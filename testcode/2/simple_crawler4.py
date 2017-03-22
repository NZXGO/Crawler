# -*- coding: utf-8 -*-
"""
Created on Mon Mar 20 16:19:55 2017

@author: 小甜甜
"""

from __future__ import print_function, division
import urllib2
import re
import urlparse
import datetime
import time
import lxml.html
import csv


class Throttle:
    """
        下载延迟类
    """
    def __init__(self, delay):
        self.delay = delay
        self.demains = {}
        
    def wait(self, url):
        """
        这种做法有点叼啊，应对那种分布式的服务器
        """
        #获取服务器位置信息
        domain = urlparse.urlparse(url).netloc
        last_accessed = self.demains.get(domain)
        
        if self.delay > 0 and last_accessed is not None:
            sleep_secs = self.delay - (datetime.datetime.now()-last_accessed).seconds
            if sleep_secs > 0:
                time.sleep(sleep_secs)                         
        self.demains[domain] = datetime.datetime.now()
         
        
class ScrapeCallback:
    """
        回调类,负责抽取网页中感兴趣的内容，并将之保存到.csv文件
    """
    def __init__(self):
        self.writer = csv.writer(open('countries.csv', 'w'))
        self.fields = ('area', 'population', 'iso', 'country', 'capital',
          'continent', 'tld', 'currency_code', 'currency_name', 'phone',
          'postal_code_format', 'postal_code_regex', 'languages',
          'neighbours')
        self.writer.writerow(self.fields)
        
    def __call__(self, url, html):
        if re.search('/view/', url):
            tree = lxml.html.fromstring(html)
            row = []
            for field in self.fields:
                #print(field)
                row.append(tree.cssselect(
                'table > tr#places_%s__row > td.w2p_fw' % field
                )[0].text_content())
            self.writer.writerow(row)

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


def crawl_sitemap(url):
    """
    通过网络地图文件，获取该网站涉及到的链接（通常不全）
    """
    sitemap = download(url)
    links = re.findall('<loc>(.*?)</loc>', sitemap)
    for link in links:
        print( 'observed url : ', link )
        #html = download(link)
        #..


def get_links(html):
    """
    通过正则表达式在页面中寻找符合要求的链接标签
    """
    webpage_regex = re.compile('<a[^>]+href=["\'](.*?)["\']', re.IGNORECASE)
    return webpage_regex.findall(html)


def link_crawler(seed_url, link_regex, delay=0.5, max_depth=2, scrape_callback=None):
    """
    广度优先搜索，寻找页面中的所有链接并下载
    """
    crawl_queue = [seed_url]
    #用字典的方式记录已访问链接的深度
    seen_link = { seed_url:0 }
    throttle = Throttle(delay = delay)
    
    while crawl_queue:
        url = crawl_queue.pop()
        throttle.wait(url)
        html = download(url)
        
        if scrape_callback:
            scrape_callback(url, html)
        
        depth = seen_link[url]
        if depth>=0 and depth<max_depth:
            for link in get_links(html):
                #link为相对路径
                if re.match(link_regex, link):
                    #print( link )
                    #将相对路径link补全
                    link = urlparse.urljoin(seed_url, link)
                    if link not in seen_link:
                        seen_link[link] = depth+1
                        crawl_queue.append(link)




#print download('http://httpstat.us/500')
#print( download('http://meetup.com') )
#crawl_sitemap('http://example.webscraping.com/sitemap.xml')
crawl_results = link_crawler('http://example.webscraping.com', '/(index|view)', 
             scrape_callback=ScrapeCallback())

#print( download('http://www.baidu.com/robots.txt') )
#crawl_sitemap('http://www.baidu.com/sitemap.xml')





