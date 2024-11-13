#!/usr/bin/env python3
#
import xml.etree.ElementTree as ET
tree = ET.parse('blog-dump.xml')
root = tree.getroot()

posts = root.findall('{http://www.w3.org/2005/Atom}entry')

# print("p")
# p = posts[0]
# print (list(p))
# 
# print("q")
# q=p[0]
# print(q.text)

for p in posts:
  q = p[0]
  qt = q.text
  if(qt.find("post-")):
    print(qt)
    exit()
