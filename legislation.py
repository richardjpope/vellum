import re
import urllib
import pprint
from bs4 import BeautifulSoup
from operator import itemgetter
import feedparser
#
# def parse_text(text):

def parse_query(text):

    chars_per_goat = 36283

    response = {}

    #title & other legislation
    legislation = re.findall('[A-Z].*[Act|Bill] [1-9][0-9][0-9][0-9]', text)
    response['title'] = legislation[0]
    response['other_legislation'] = []
    for item in legislation:
        item_cleaned = re.sub(".*section [0-9A-B]* of the ", "", item)
        item_cleaned = re.sub("Part [0-9] of the", "", item_cleaned)
        item_cleaned = re.sub("[A-B]\) of the ", "", item_cleaned)

        if item_cleaned != response['title'] and item_cleaned not in response['other_legislation'] and len(item_cleaned) <= 50:
            response['other_legislation'].append(item_cleaned)

    #description
    description = re.findall('An Act [^\.]*\.', text)
    response['description'] = description[0]

    #regulations
    response['regulations'] = []
    regex = re.compile('Regulations may [prescribe|provide|specify|make such provision|make provision|for the purpose|for any purpose][^\.]*', re.MULTILINE)
    response['regulations'] = re.findall(regex, text)

    #definitions
    response['definitions'] = []
    regex = re.compile(u'[\u201c|"][0-9a-zA-Z_|\s]*[\u201d|"] means[^\.]*', re.UNICODE)
    response['definitions'] = re.findall(regex, text)

    #ministerial
    response['ministerial_rights'] = []
    regex = re.compile('The Secretary of State may [^not][^\.]*', re.MULTILINE+re.IGNORECASE)
    response['ministerial_rights'] = re.findall(regex, text)

    response['ministerial_responsibilities'] = []
    regex = re.compile('The Secretary of State may not[^\.]*', re.MULTILINE+re.IGNORECASE)
    may_not = re.findall(regex, text)
    regex = re.compile('The Secretary of State must[^\.]*', re.MULTILINE+re.IGNORECASE)
    must = re.findall(regex, text)
    regex = re.compile('^The Secretary of State shall[^\.]*', re.MULTILINE+re.IGNORECASE)
    shall = re.findall(regex, text)
    response['ministerial_responsibilities'] = may_not + must + shall


    #stats
    response['vellum_count'] = float((len(text)) / float(chars_per_goat)) * 2.0
    response['word_count'] = len(text.split(' '))


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
