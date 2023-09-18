# -*- coding: utf-8 -*-
"""
Created on Thu Sep 14 12:48:13 2023

@author: romain.coulon
"""

# import xml.etree.ElementTree as ET

# tree = ET.parse("Ce-139_database_FAIR.xml")
# root = tree.getroot()

# for element in root.iter('dsi:unit'):
#     print(element.text)

# for element in root.findall('Comparison_data'):
#     value = element.find('dsi:unit').text
#     print(value)

from bs4 import BeautifulSoup
import requests

xml = open("Ce-139_database_FAIR.xml")

soup = BeautifulSoup(xml,"xml")
# soup.prettify()
xml_tag = soup.find_all('Method')
for i in xml_tag:
    print(i.string)

# 


xml.close()