import requests
import urllib.parse
from bs4 import BeautifulSoup
from config import sa_key
from replit import db

'''
TODO
1. Обходить cloudflare -> нашёл ресурс, который за меня это выполняет -> он ограничен -> Только для себя (1000 ссылок/мес)?
2. Доставать страницы (
    -они все начинаются на i3/i5/i7? Есть ли разница в цифре? -> Буду тестить -> Разницы нет -> видимо, подстраховка
    -Проблема с тем, что файлы пикч могут кончаться на .png -> Нужно проверять на существование такой пикчи перед отправлению ТГ
    )
3. Заливать страницы в тг (
    -по ссылке на галлерею?
    -Сделать эмулятор сайта в виде инлайн-меню? -> как сделать инлайн-меню без aoigram? Расход ресурса?
    -Заливать ссылки в тг или сами .jpeg? -> ссылки неудобно смотреть, .jpeg расходует много трафика -> Проблема решена sendPhoto -> sendMediaGroup
    )
'''


def find_manga(index_manga):
    if index_manga not in db:
        sa_api = 'https://api.scrapingant.com/v2/general'
        q_params = {'url': f'https://nhentai.net/g/{index_manga}/', 'x-api-key': sa_key}
        req_url = f'{sa_api}?{urllib.parse.urlencode(q_params)}'
      
        r = requests.get(req_url)
      
        soup = BeautifulSoup(r.content, 'lxml')
      
        number_of_pages = int(soup.find('section', id='tags').find_all('div')[7].find(class_='name').text)
        print(number_of_pages)
        gal = soup.find(itemprop="image")['content'].split('//')[1].split('/')[2]
        print(gal)
        link = 'https://i7.nhentai.net/galleries/' + gal + '/{}.jpg'
        db[index_manga] = (link, number_of_pages)
    else:
        link, number_of_pages = db[index_manga]
    return link, number_of_pages

