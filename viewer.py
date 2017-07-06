# -*- coding: utf-8 -*-

import argparse
import pickle
from settings import DATA_PATH
from dateparser import parse
from lxml import etree

parser = argparse.ArgumentParser(description='Number of articles.')
parser.add_argument(
    '--date', required=True, help='aritcles to be showed for date', type=parse
)
args = parser.parse_args()
pubdate = args.date.date()


def get_articles(pubdate):
    articles = []

    with open(DATA_PATH, 'r') as data_file:
        for article in pickle.load(data_file):
            if article['pubdate'].date() == pubdate:
                articles.append(article)

    return articles


articles = get_articles(pubdate)

if len(articles) != 0:
    print "%s news found" % len(articles)
    print '\n\n'

    for article in articles:
        print str(article['pubdate'].strftime("%Y-%m-%d %H:%M")) + '  ' + unicode(article['title'])
        print '\n'
        print unicode(article['link'])
        print '\n'
        body = str(article['body'])
        html = etree.HTML(body.decode('utf-8'))
        for p in html.xpath(u'//p[not(contains(., "гиперссылка обязательна"))]//text()'):
            print p
            print unichr(2029)
        print '\n\n'
else:
    print "Sorry, for " + str(pubdate) + " no news found"
