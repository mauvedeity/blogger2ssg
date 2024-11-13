#!/usr/bin/env python3
#
import xml.etree.ElementTree as ET
from datetime import datetime
import os
import time
#
#
def getPostID(pstr):
  return(pstr.split('-')[2])

def titleUnmung(pstr):
  sl = str(pstr).splitlines()
  if(len(sl)== 1):
    return(sl[0])
  else:
    rv = ''
    for i in sl:
      rv += i.strip() + ' '
    return(rv.strip())

def processEntry(entry):
  etitle = entry.find('{http://www.w3.org/2005/Atom}title').text
  econtent = entry.find('{http://www.w3.org/2005/Atom}content').text
  epubdate = entry.find('{http://www.w3.org/2005/Atom}published').text
  epubid = entry.find('{http://www.w3.org/2005/Atom}id').text
  if (etitle == None): # one post doesn't have a title
    etitle = epubid
  print(titleUnmung(etitle), getPostID(epubid),sep='|')
  fname = getPostID(epubid) + '.html'
  with open(fname, 'wt') as outf:
    outf.write('<h1>' + etitle + '</h1>\n')
    outf.write('\n')
    outf.write(econtent)
    outf.write('\n')
  tm = datetime.strptime(epubdate,'%Y-%m-%dT%H:%M:%S.%f%z')
  os.utime(fname,(tm.timestamp(),tm.timestamp()))

def main():
  tree = ET.parse('blog-dump.xml')
  root = tree.getroot()
  entries = root.findall('{http://www.w3.org/2005/Atom}entry')

  ekount = 0
  for e in entries:
    e_id = e.find('{http://www.w3.org/2005/Atom}id').text
    if 'post-' in e_id:
      processEntry(e)
      ekount += 1
      if(ekount > 10):
        exit()

if __name__ == '__main__':
  main()
