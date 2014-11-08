import re
import urllib
import pprint
from bs4 import BeautifulSoup
from operator import itemgetter
import feedparser
#
# def parse_text(text):

def parse_query(text):

    response = {}

    #title[Act|Bill] [0-9][0-9][0-9][0-9]
    legislation = re.findall('[A-Z].*[Act|Bill] [1-9][0-9][0-9][0-9]', text)
    response['title'] = legislation[0]

    #description
    description = re.findall('An Act to [^\.]*\.', text)
    response['description'] = description[0]


    #regulations
    response['regulations'] = []
    regex = re.compile('Regulations may [prescribe|provide|specify|make such provision|make provision|for the purpose|for any purpose][^\.]*', re.MULTILINE)
    response['regulations'] = re.findall(regex, text)

    #definitions
    response['definitions'] = []
    regex = re.compile(u'[\u201c|"][0-9a-zA-Z_|\s]*[\u201d|"] means[^\.]*', re.UNICODE)
    response['definitions'] = re.findall(regex, text)

    return response

def parse_legislation(url):
    response = {}
    data_url = '%s/data.xml' % url
    data = urllib.urlopen(data_url).read()
    soup = BeautifulSoup(data)

    #title and desctiption
    response['title'] = soup.find_all('dc:title')[0].string
    response['description'] = soup.find_all('dc:description')[0].string

    #regulations
    response['regulations'] = []
    regex = re.compile('Regulations may prescribe|provide|specify|make such provision|make provision|for the purpose|for any purpose')
    regulations = soup.find_all('text', text = regex)
    for regulation in regulations:
        response['regulations'].append(regulation.string)

    #definitions
    response['definitions'] = []
    regex = re.compile(u'([0-9a-zA-Z_])*\u201d means.*', re.UNICODE)
    definitions = soup.find_all('text', text = regex)
    #definitions = soup.find_all('term')
    for definition in definitions:
        print definition.parent
        response['definitions'].append({'term': definition.string.capitalize(), 'definition': definition.parent.contents[2].replace(u'\u201d ', u'')})
        # print regex.match(unicode(definition.string))

    response['definitions'].sort(key=itemgetter('term'))

    return response

def parse_bill(url):
    response = {}
    html = urllib.urlopen(url).read()
    soup = BeautifulSoup(html)

    #title
    response['title'] = soup.select("h1")[0].string

    #rss
    rss_feed = "http://services.parliament.uk%s" % soup.select("li.rss a")[0]['href']
    feed = feedparser.parse(rss_feed)
    response['description'] = feed["channel"]["description"]

    #content
    return response
