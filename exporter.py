#!/usr/bin/env python3
#
import xml.etree.ElementTree as ET
tree = ET.parse('blog-dump.xml')
root = tree.getroot()

posts = root.findall('{http://www.w3.org/2005/Atom}entry')

p = posts[0]
print (list(p))

q=p[0]
print(q.text)
