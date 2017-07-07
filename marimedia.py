# -*- coding: utf-8 -*-

import requests
from lxml import etree
from dateparser import parse
from datetime import datetime, date
import argparse
import pickle
from settings import DATA_PATH
import marimedia_parse_article

def generate_urls(base_url):
    yield base_url
    page_num = 2
    while True:
        yield base_url + '?p=%s' % page_num
        page_num += 1


def parse_newsline(page_html):
    for item in page_html.cssselect('article.news_item'):
        article_url = str(item.xpath('.//a[@class = "news_title"]/@href')[0])
        yield {
            'link': article_url,
            'title': item.cssselect('.news_title')[0].text,
            'pubdate': parse(item.cssselect('.date')[0].text),
            'description': item.cssselect('.small-desc')[0].text,
            'category': item.cssselect('.category')[0].text,
            'body': marimedia_parse_article.parse_article(article_url)['body']
        }

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Number of articles.')
    parser.add_argument(
        '--articles_count', required=True, help='number of aritcles to be fetched', type=int
    )
    args = parser.parse_args()

    articles_count = args.articles_count

    today = date.today()
    base_url = today.strftime('http://www.marimedia.ru/news/archive/%Y/%m/')

    articles = []

    for url in generate_urls(base_url):
        page_text = requests.get(url).text
        page_html = etree.HTML(page_text)
        page_links = page_html.cssselect('article.news_item')

        for article in parse_newsline(page_html):

            if len(articles) == articles_count:
                with open(DATA_PATH, 'w+') as data_file:
                    print articles
                    pickle.dump(articles, data_file)
                    print "Data saved!"
                    print '\n'

                exit()

            articles.append(article)
