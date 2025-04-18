#!env python3

strURLFrom = 'https://uselessofblog.blogspot.com'
strURLTo = '../..q'

from html.parser import HTMLParser

class MyHTMLParser(HTMLParser):
    def handle_starttag(self, tag, attrs):
        print("Encountered a start tag:", tag, "with attrs ", attrs)
        # if the tag is an A, then look at the atts and parse
        if (tag == 'a'):
            attrlist = attrs
            print('a', attrlist[0])
            hr, data = attrlist[0]
            print(data)
            data = data.replace(strURLFrom, strURLTo)
            print(data)

    def handle_endtag(self, tag):
        print("Encountered an end tag :", tag)

    def handle_data(self, data):
        print("Encountered some data  :", data)

parser = MyHTMLParser()

with open('it-was-all-going-so-well.html','r') as htmlsrc:
    htmlcontent = htmlsrc.read()

# print(htmlcontent)
parser.feed(htmlcontent)
