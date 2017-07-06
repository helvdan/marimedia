# *-* coding: utf-8 *-*

import requests
from lxml import etree
import argparse

ARTICLES_URLS = ['http://www.marimedia.ru/news/yola/item/63046/', 'http://www.marimedia.ru/news/politics/item/63000/']

articles_contents = []


def parse_article(url):
    article_text = requests.get(url).text
    article_html = etree.HTML(article_text)
    return {
        'title': article_html.cssselect('#news-title')[0].text,
        'body': etree.tostring(article_html.cssselect('.news-text')[0], encoding="UTF-8", method='html')
    }

#
#
#
#
#

# for url in ARTICLES_URLS:
#     articles_contents.append(parse_article(url))
#
# for article in articles_contents:
#     print article['body']

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='URL')
    parser.add_argument(
        '--url', required=True, help='url to be parse', type=str
    )
    args = parser.parse_args()

    url = args.url

    article = parse_article(url)

    print article['title']
    print '\n'
    print article['body'].strip()
