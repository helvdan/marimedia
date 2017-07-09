# -*- coding: utf-8 -*-

import argparse
import pickle
from settings import DATA_PATH
from dateparser import parse
from lxml import etree


class Viewer(object):

    def __init__(self):
        with open(DATA_PATH, 'r') as data_file:
            self.articles = pickle.load(data_file)

    def _filter_articles(self, pubdate):
        return [
            article
            for article in self.articles
            if article['pubdate'].date() == pubdate
        ]

    def print_articles(self, pubdate, text_length=100):
        articles = self._filter_articles(pubdate)
        articles_count = len(articles)

        if not articles_count:
            print u'Извините, новостей за %s не найдено' % pubdate
            return

        print u'За %s найдено %s новостей\n' % (pubdate, articles_count)
        for article in articles:
            print u'{pubdate} {title}'.format(**article)
            print article['link']
            body = str(article['body'])
            html = etree.HTML(body.decode('utf-8'))
            for p in html.xpath(u'//p[not(contains(., "гиперссылка обязательна"))]//text()'):
                if not p:
                    continue

                while p:
                    print '\t' + p[:text_length]
                    p = p[text_length:]
            print ''


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Number of articles.')
    parser.add_argument(
        '--date', required=True, help='aritcles to be showed for date', type=parse
    )
    args = parser.parse_args()
    pubdate = args.date.date()

    viewer = Viewer()
    viewer.print_articles(pubdate)
