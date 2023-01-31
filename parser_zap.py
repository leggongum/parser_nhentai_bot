import requests
#import urllib.parse
from bs4 import BeautifulSoup
#from config import sa_key
from replit import db


def find_manga(index_manga):
    if index_manga not in db:
        #sa_api = 'https://api.scrapingant.com/v2/general'
        #q_params = {'url': f'https://hentaizap.com/gallery/{index_manga}/', 'x-api-key': sa_key}
        #req_url = f'{sa_api}?{urllib.parse.urlencode(q_params)}'
        r = requests.get(f'https://hentaizap.com/gallery/{index_manga}/')
        soup = BeautifulSoup(r.content, 'lxml')

        number_of_pages = int(soup.find('span', class_='info_pg').text.split()[1])
        print(number_of_pages)

        pattern_link = soup.find_all('img')[3]['data-src'].split('.')
        link = pattern_link[0] + '.' + pattern_link[1] + '.' + pattern_link[2][:-2] + '{}' + '.' + pattern_link[3]
        print(link)

        #db[index_manga] = (link, number_of_pages)

    else:
        link, number_of_pages = db[index_manga]
    return link, number_of_pages
