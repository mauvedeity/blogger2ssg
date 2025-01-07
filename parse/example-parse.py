#!env python3

from html.parser import HTMLParser

class MyHTMLParser(HTMLParser):
    def handle_starttag(self, tag, attrs):
        print("Encountered a start tag:", tag, " with attrs ", attrs)

    def handle_endtag(self, tag):
        print("Encountered an end tag :", tag)

    def handle_data(self, data):
        print("Encountered some data  :", data)

parser = MyHTMLParser()

with open('another-hurdle-for-cryptocurrencies.html','r') as htmlsrc:
    htmlcontent = htmlsrc.read()

print(htmlcontent)
parser.feed(htmlcontent)
