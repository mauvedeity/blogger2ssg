#!/usr/bin/env python3
#
import xml.etree.ElementTree as ET
tree = ET.parse('blog-dump.xml')
root = tree.getroot()

for child in root:
  print(child.tag, child.attrib)


