#!/usr/bin/env python3
#
import xml.etree.ElementTree as ET
from datetime import datetime
import os
import time
##
#
def getPostID(pstr):
  return(pstr.split('-')[2])

def splitup(pspath):
  lpath = pspath.split('/')
  return(lpath[-3], lpath[-2], lpath[-1])
  
def requiredir(lpf):
  newdir = '/'.join(lpf)
  newdir = './output/'+newdir+'/'
  newdir = os.path.normpath(newdir)
  os.makedirs(newdir,exist_ok=True)

def getValue(pentry, pname):
  pnam2 = '{http://www.w3.org/2005/Atom}'+pname
  return(pentry.find(pnam2).text)

def getPathTitle(pentry):
  epath = None
  etitle = None
  links = pentry.findall('{http://www.w3.org/2005/Atom}link')
  for l in links:
    if(l.attrib['rel'] == 'alternate'):
      epath = l.attrib['href']
      etitle = l.attrib['title']
  return(epath, etitle)  

def fixcontent(pcontent):
  """
  cmd = 'pandoc -f html -t markdown -o target.md source.html'
  lcmd = cmd.split('')
  lcmd[6] = target
  lcmd[7] = source
  """
  return(pcontent)

#
# POSTS
#
def processPost(entry):
  epubid = getValue(entry, 'id')
  econtent = getValue(entry, 'content')
  epubdate = getValue(entry,'published')
  epath = None
  etitle = None
  epath, etitle = getPathTitle(entry)

  if(epath is None):
    eyear = '0000'
    emonth= '00'
    fname = epubid.split('-')[-1]
  else:
    eyear, emonth, fname = splitup(epath)
    
  fname = "./output/" + eyear + "/" + emonth + "/" + fname
  requiredir([eyear, emonth])

  if (etitle == None): # one post doesn't have a title
    etitle = epubid
  with open(fname, 'wt') as outf:
    outf.write('<h1>' + etitle + '</h1>\n')
    outf.write('\n')
    outf.write(fixcontent(econtent))
    outf.write('\n')
  tm = datetime.strptime(epubdate,'%Y-%m-%dT%H:%M:%S.%f%z')
  os.utime(fname,(tm.timestamp(),tm.timestamp()))

#
# PAGES
#
def processPage(entry):
  epubid = getValue(entry, 'id')
  econtent = getValue(entry, 'content')
  epubdate = getValue(entry,'published')
  epath = None
  etitle = None
  epath, etitle = getPathTitle(entry)
  requiredir(['p'])
  fname = './output/p/'+epubid.split('-')[-1]
  with open(fname, 'wt') as outf:
    outf.write('<h1>' + etitle + '</h1>\n\n')
    outf.write(fixcontent(econtent))
    outf.write('\n')
  tm = datetime.strptime(epubdate,'%Y-%m-%dT%H:%M:%S.%f%z')
  os.utime(fname,(tm.timestamp(),tm.timestamp()))

#
# MAIN
#
def main():
  tree = ET.parse('./input/blog-dump.xml')
  root = tree.getroot()
  entries = root.findall('{http://www.w3.org/2005/Atom}entry')

  ekount = 1
  EKMAX = 20  # Don't dump all 700 entries
  for e in entries:
    e_id = getValue(e, 'id')
    if 'post-' in e_id:
      processPost(e)
      ekount += 1
    if 'page-' in e_id:
      processPage(e)
      ekount += 1
    if(ekount >= EKMAX):
      break
  
  print(ekount,'entries processed')

if __name__ == '__main__':
  main()
