#!/usr/bin/env python3
#
import xml.etree.ElementTree as ET
from datetime import datetime
import os
import time
import subprocess
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

def fixcontent(pcontent: str, ptitle: str, pdate):
  result = subprocess.run(['pandoc', '-f', 'html', '-t', 'markdown'], input=pcontent, capture_output=True, text=True)
  process2 = '+++\n'
  process2 += f"title = '{ptitle}'\n"
  process2 += f"date = '{pdate}'\n"
  process2 += "draft = 'true'\n"
  process2 += '+++\n\n'
  process2 += result.stdout
  # additional processing
  process2 = process2.replace('{target="_new"}','')
  process2 = process2.replace('{target="_blank"}','')
  process2 = process2.replace('\\"','"')
  process2 = process2.replace("\\'", "'")
  process2 = process2.replace("\\", "")
  process2 = process2.replace('https://uselessofblog.blogspot.com/p/proudly-serving.html','/pages/proudly-serving/')
  return(process2)
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

  # fname = "./output/" + eyear + "/" + emonth + "/" + fname + ".md"
  # requiredir('./output/')
  requiredir("./output")
  fname = fname.replace('.html', '.md')
  fname = f"./output/{fname}"
  if (etitle == None): # one post doesn't have a title
    etitle = epubid
  with open(fname, 'wt') as outf:
    outf.write(fixcontent(econtent, etitle, epubdate))
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
    outf.write(fixcontent(econtent, etitle, epubdate))
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
  EKMAX = 2500  # Don't dump all 700 entries
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
