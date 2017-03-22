# -*- coding: utf-8 -*-
"""
Created on Mon Mar 20 16:19:55 2017
LXML基本使用
@author: 小甜甜
"""

from __future__ import print_function, division
import csv


FIELDS = ('area', 'population', 'iso', 'country', 'capital',
          'continent', 'tld', 'currency_code', 'currency_name', 'phone',
          'postal_code_format', 'postal_code_regex', 'languages',
          'neighbours')

writer = csv.writer(open('countriesddd.csv', 'w'))
writer.writerow(FIELDS)
writer.writerow(FIELDS)
writer.writerow(FIELDS)





