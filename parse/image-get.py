#!env python3

import urllib.request
import shutil
from os.path import basename, exists
from html.parser import HTMLParser

# Global URL header
#
glHeader = ''

# HTML Parser
#
class myHTMLParser(HTMLParser):
    def handle_starttag(self, tag, attrs):
        if(tag == 'img'):
            for attr in attrs:
                if attr[0] == 'src':
                    srcname = attr[1]
            if exists('dest/'+srcname):     ## hardwired, plz fix
                print('Skipped', srcname)
            else:
                print('Fetching',srcname)
                url2file(srcname, 'dest')   ## hardwired, plz fix
    def handle_endtag(self, tag):
        pass
    def handle_data(self, data):
        pass

# Image Grabber
#
def url2file(sURL, sDestPath):
    sDest = sDestPath + '/' + basename(sURL)
    sURL = glHeader + sURL
    with urllib.request.urlopen(sURL) as response, open(sDest,'wb') as outfile:
        data = response.read()
        outfile.write(data)

def getAllImages(sURL):
    sURL = glHeader + sURL
    with urllib.request.urlopen(sURL) as response:
        data = response.read()
        print(data)
        indexdata = data.decode("utf-8")
        parser = myHTMLParser()
        parser.feed(indexdata)

if __name__ == '__main__':
    glHeader = 'http://localhost:8091/'
    getAllImages('index.html')
