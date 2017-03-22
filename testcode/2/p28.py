# -*- coding: utf-8 -*-
"""
Created on Mon Mar 20 16:19:55 2017
Beautiful Soup基本使用
@author: 小甜甜
"""

from __future__ import print_function, division
from bs4 import BeautifulSoup


broken_html = '<ul class=country><li>Area<li>Population</ul>'
soup = BeautifulSoup(broken_html, 'html.parser')
fixed_html = soup.prettify()
print(fixed_html)

ul = soup.find('ul', attrs={'class':'country'})
print( ul )
ul = soup.find('li')
print( ul )
ul = soup.find_all('li')
print( ul )


