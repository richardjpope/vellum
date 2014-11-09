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
    response['title'] = ''
    legislation = re.findall('[A-Z].*[Act|Bill] ?[1-9]?[0-9]?[0-9]?[0-9]?', text)
    if legislation:
        response['title'] = legislation[0]

    legislation = re.findall('[A-Z].*Act [1-9][0-9][0-9][0-9]', text)
    response['other_legislation'] = []
    for item in legislation:
        item_cleaned = re.sub(".*section [0-9A-B]* of the ", "", item)
        item_cleaned = re.sub("Part [0-9] of the", "", item_cleaned)
        item_cleaned = re.sub("[A-B]\) of the ", "", item_cleaned)

        if item_cleaned != response['title'] and item_cleaned not in response['other_legislation'] and len(item_cleaned) <= 50:
            response['other_legislation'].append(item_cleaned)

    #description
    response['description'] = ''
    description = re.findall('An Act to[^\.]*\.', text, re.MULTILINE+re.IGNORECASE)
    if description:
        response['description'] = description[0]
    else:
        description = re.findall('Bill to[^\.]*\.', text, re.MULTILINE+re.IGNORECASE+re.UNICODE)
        if description:
            response['description'] = description[0]

    #regulations
    response['regulations'] = []
    regex = re.compile('Regulations may [prescribe|provide|specify|make such provision|make provision|for the purpose|for any purpose][^\.]*', re.MULTILINE+re.IGNORECASE)
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
