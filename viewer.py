# -*- coding: utf-8 -*-

import argparse
import pickle
from settings import DATA_PATH
from dateparser import parse

parser = argparse.ArgumentParser(description='Number of articles.')
parser.add_argument(
    '--date', required=True, help='aritcles to be showed for date', type=parse
)
args = parser.parse_args()
pubdate = args.date.date()

with open(DATA_PATH, 'r') as data_file:

    output = []

    for article in pickle.load(data_file):
        if article['pubdate'].date() == pubdate:
            output.append(article)

    if len(output) != 0:
        print "%s news found" % len(output)

        for article in output:
            print str(article['pubdate'].strftime("%Y-%m-%d %H:%M")) + '  ' + unicode(article['title'])
            print unicode(article['link'])
            print str(article['body'])
    else:
        print "Sorry, for " + str(pubdate) + " no news found"
