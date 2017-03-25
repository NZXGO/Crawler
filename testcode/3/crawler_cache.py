# -*- coding: utf-8 -*-
"""
Created on Thu Mar 23 19:54:23 2017

@author: 小甜甜
"""

import DownLoader
import DiskCache
import csv
import lxml.html

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
            
def get_links(html):
    """
    通过正则表达式在页面中寻找符合要求的链接标签
    """
    webpage_regex = re.compile('<a[^>]+href=["\'](.*?)["\']', re.IGNORECASE)
    return webpage_regex.findall(html)

def link_crawler(seed_url, link_regex, delay=0.5, max_depth=2, scrape_callback=None, cache_dir='cache'):
    """
    广度优先搜索，寻找页面中的所有链接并下载
    """
    crawl_queue = [seed_url]
    #用字典的方式记录已访问链接的深度
    seen_link = { seed_url:0 }
    cache = DiskCache.DiskCache(cache_dir=cache_dir)
    D = DownLoader.DownLoader(delay=delay, cache=cache)
    
    while crawl_queue:
        url = crawl_queue.pop()
        html = D(url)
        
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
                        
                        
                        
crawl_results = link_crawler('http://example.webscraping.com', '/(index|view)', 
             scrape_callback=ScrapeCallback(), max_depth=100)