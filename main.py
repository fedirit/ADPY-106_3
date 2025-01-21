import json
import bs4
import requests
import time
from fake_headers import Headers
from pprint import pprint
KEYWORDS = ['дизайн', 'фото', 'web', 'python']

# не хватает предварительно проведенного вебинара по html, программа написана на фоне неполного понимания html,
# без опыта
# такого использования

def get_fake_headers():
    return Headers(browser='chrome', os='mac').generate()

response = requests.get('https://habr.com/ru/all/', headers=get_fake_headers())
soup = bs4.BeautifulSoup(response.text, features="lxml")

time.sleep(7) # ожидание полной прогрузки веб-страницы, иначе выдает ошибки, иногда при выкладке в ленту новой
                # статьи бывают более длительные задержки, но после вебинара, знаний полученных
                # на уроке пока недостаточно
                # поэтому сделал задержку, с надеждой что этого будет достаточно, НО не всегда,
                # порой выкладка новой статьи более 30 сек

news_list = soup.find_all('article', class_='tm-articles-list__item')

for news in news_list:
    article_preview_name = news.find('h2').text
    article_preview_link = news.find('a',
                                class_='tm-article-datetime-published tm-article-datetime-published_link')['href']
    article_time = news.find('time')['title']
    article_text_preview = news.find('div',
                                class_='article-formatted-body article-formatted-body article-formatted-body_version-2')

    full_search_string = ''
    full_search_string = full_search_string + article_preview_name

    if article_text_preview == None:
        # https://habr.com/ru/companies/piter/articles/873530/ - описание данного условия
        # https://habr.com/ru/companies/ruvds/articles/873444/
        article_text_preview = news.find('div',
                                class_='article-formatted-body article-formatted-body article-formatted-body_version-1')
        full_search_string = full_search_string + str(article_text_preview)
    else:
        article_text_preview_def = article_text_preview.find_all('p')
        for article_text_preview_def_string in article_text_preview_def:
            full_search_string = full_search_string + article_text_preview_def_string.text

    full_search_string_adaptive = full_search_string.lower()

    res = any(elem in full_search_string_adaptive for elem in KEYWORDS)

    if res == True:
        # print(full_search_string_adaptive)
        print(f'{article_time} - {article_preview_name} - {'https://habr.com'+article_preview_link}')