# -*- coding: utf-8 -*-
from dateparser import parse

# 1. Создать репозиторий на github
# 2. Создавать ссылку типа http://www.marimedia.ru/news/archive/2017/07/ динамически, исходя из текущей даты
# 3. Собирать новости только из новостной ленты
# 4. Собрать не просто ссылки, а структуру типа:
# [
#     {
#         'title': "В Марий Эл объявлено штормовое предупреждение",
#         'description': "5 и 6 июля на территории республики ожидаются гроза и шквалистый ветер до 20 м/с.",
#         'pubdate': datetime(year=2017, month=7, day=5, hour=11, minute=2),
#         'category': 'ПОГОДА'
#     },
#     {
#         'title': "Вячеслав Зотин вернулся в политику",
#         'description': "Александр Евстифеев подписал указ об утверждении В. М. Зотина членом Общественной палаты Республики Марий Эл.",
#         'pubdate': datetime(year=2017, month=7, day=5, hour=10, minute=3),
#         'category': 'ПОЛИТИКА'
#     }
#     ...
# }
# 5. Собирать с первых 3-х страниц (http://www.marimedia.ru/news/archive/2017/07/, http://www.marimedia.ru/news/archive/2017/07/?p=2, http://www.marimedia.ru/news/archive/2017/07/?p=3)
# 6. Сделать ограничение по количеству статей, количество страниц пагинации убрать. Значение количества статей передавать через обязательный параметр в командной строке.
# 6.5 Выводиться должно по шаблону 17:00  Заголовок новости
# 7. Сохранить данные на диск

import requests
from lxml import etree
from datetime import datetime, date


def generate_urls(count, base_url):
    output = []

    output.append(base_url)
    for x in range(2, count + 1):
        output.append(base_url + '?p=%s' % x)

    return output


def parse_newsline(page_html):
    for item in page_html.cssselect('article.news_item'):
        yield {
            'link': item.get('href'),
            'title': item.cssselect('.news_title')[0].text,
            'pubdate': parse(item.cssselect('.date')[0].text),
            'description': item.cssselect('.small-desc')[0].text,
            'category': item.cssselect('.category')[0].text
        }


NUMBER_OF_PAGES = 3

today = date.today()
base_url = today.strftime('http://www.marimedia.ru/news/archive/%Y/%m/')

articles = []

for url in generate_urls(NUMBER_OF_PAGES, base_url):
    page_text = requests.get(url).text
    page_html = etree.HTML(page_text)
    page_links = page_html.cssselect('article.news_item')

    for article in parse_newsline(page_html):
        articles.append(article)

for article in articles:
    print str(article['pubdate']) + ' ' + article['title']
