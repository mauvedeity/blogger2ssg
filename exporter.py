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

def splitup(pspath):
  lpath = pspath.split('/')
  return(lpath[-3], lpath[-2], lpath[-1])

def requiredir(pf1, pf2):
  newdir = './' + pf1 + '/' + pf2
  os.makedirs(newdir,exist_ok=True)

def processEntry(entry):
  epubid = entry.find('{http://www.w3.org/2005/Atom}id').text
  econtent = entry.find('{http://www.w3.org/2005/Atom}content').text
  epubdate = entry.find('{http://www.w3.org/2005/Atom}published').text

  epath = None
  etitle = None

  links = entry.findall('{http://www.w3.org/2005/Atom}link')
  for l in links:
    if(l.attrib['rel'] == 'alternate'):
      epath = l.attrib['href']
      etitle = l.attrib['title']

  if(epath is None):
    eyear = '0000'
    emonth= '00'
    fname = epubid.split('-')[-1]
  else:
    eyear, emonth, fname = splitup(epath)
    fname = "./" + eyear + "/" + emonth + "/" + fname

  requiredir(eyear, emonth)

  if (etitle == None): # one post doesn't have a title
    etitle = epubid
  print(etitle, getPostID(epubid),sep='|')
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
      if(ekount > 1000):
        exit()

if __name__ == '__main__':
  main()
