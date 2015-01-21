import urllib2
import xml.sax
import email.utils
from xml.dom import minidom
from xml.dom.minidom import parse, parseString
from datetime import datetime

DEMOCRACYNOW='http://www.democracynow.org/podcast-video.xml'

def _getText(root, elName):
    return root.getElementsByTagName(elName)[0].firstChild.data

def _getAttribute(root, elName, attr):
    return root.getElementsByTagName(elName)[0].getAttribute(attr)

def parseDate(dateString):
    date_tz = email.utils.parsedate_tz(dateString);  
    return datetime(*date_tz[:6]);

def fetchChannel():
    channel = {}
    itemList = []
    response = urllib2.urlopen(DEMOCRACYNOW)
    content = response.read()
    response.close()  # best practice to close the file
    doc = minidom.parseString(content)

    channel['title'] = _getText(doc, "title")

    items = doc.getElementsByTagName("item")
    for item in items:
        pubDate = parseDate(_getText(item, "pubDate"))
        itemDict = {
            'title': _getText(item, "title"),
            'thumbnail': _getAttribute(item, "media:thumbnail", "url"),
            'url': _getAttribute(item, "media:content", "url"),
            'pubDate': pubDate
            }
        itemList.append(itemDict)
    channel['items'] = sorted(itemList, 
                              key=lambda item: item['pubDate'], 
                              reverse=True)
    return channel

if __name__ == "__main__":
    channel = fetchChannel()
    for item in channel['items']:
        print str(item['pubDate']) + " " + item['title']
