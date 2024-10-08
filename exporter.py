#!/usr/bin/env python3
#
import re
DEHTML = re.compile('<.*?>')

import xml.etree.ElementTree as ET
tree = ET.parse('sys-cat.xml')
root = tree.getroot()

def fix_lb(lb):
    rv = lb.replace("[", ",")
    rv = rv.replace("]", ",")
    rv = rv.replace("&nbsp;", " ")
    rv = rv.replace ("&amp;", "&")
    rv = re.sub(DEHTML, '', rv)
    return(rv)

for uo in root.iter('UserObject'):
    id = uo.get('id')
    lb = fix_lb(uo.get('label'))
    lk = uo.get('link')
    print(id,lk, lb, sep=",")

