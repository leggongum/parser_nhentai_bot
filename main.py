from flask import Flask
from flask_sslify import SSLify
from flask import request
from flask import jsonify
from config import bot_token
import requests
from parser_nhen import find_manga
from time import sleep


app = Flask(__name__)
sslify = SSLify(app)

URL = f'https://api.telegram.org/bot{bot_token}/'

def send_message(chat_id, text='hihihihiiii'):
    url = URL + 'sendMessage'
    answer = {'chat_id': chat_id, "text": text}
    r = requests.post(url, json=answer)
    return r.json()


def send_photo(chat_id, photo):
    url = URL + 'sendPhoto'
    answer = {'chat_id': chat_id, 'photo': photo}
    r = requests.post(url, json=answer)
    return r.json()


def send_media_group(chat_id, media):
    url = URL + 'sendMediaGroup'
    answer = {"chat_id": chat_id, "media": media}
    r = requests.post(url, json=answer)
    print(r.json()['ok'])
    if not r.json()['ok']:
        print(r.text)
        if r.json()['error_code'] == 429:
            sleep(15)
        r = requests.post(url, json=answer)
    return r.json()


def send_manga(chat_id, index_manga):
    link, number_of_pages = find_manga(index_manga)
    inx = 1
    num_send = number_of_pages//10 
    last_send = number_of_pages%10
    sample = {"type": "photo", "media": None}
    if num_send:
        for send in range(num_send):
            media = []
            for i in range(inx, inx+10):
                new_page = sample.copy()
                new_page["media"] = link.format(i)
                media.append(new_page.copy())
            inx += 10
            send_media_group(chat_id, media)
            sleep(2)
    if last_send:
        media = []
        for i in range(inx, inx+last_send):
            new_page = sample.copy()
            new_page["media"] = link.format(i)
            media.append(new_page.copy())
        send_media_group(chat_id, media)


is_working = False

@app.route(f'/{bot_token}', methods=['POST', 'GET'])
def index():
    global is_working
    if request.method == 'POST':
        r = request.get_json()
        print(r)
        try:
            chat_id = r['message']['chat']['id']
            text = message if (message := r['message'].get('text')) else 'Принимаются только сообщения'
            
        except Exception as ex:
            send_message(chat_id=414093554, text=f'POST очень странный: {ex}')
        if is_working:
           send_message(chat_id, 'Занято! Потом напиши')
           return jsonify(r)
        try:
            if len(text) == 6 and text.isdigit():
                is_working = True
                #send_message(chat_id, 'Разгрузка бота')
                send_manga(chat_id, text)
            else:
                send_message(chat_id, 'Бот принимает только шестизначный код манги на nhentai')
        except Exception as ex:
            send_message(chat_id, f'Ошибка: {ex}')
        finally:
            is_working = False
            return jsonify(r)

    return '<h1>Flask!!</h1>'


def run():
    app.run(host="0.0.0.0", port=8000)

if __name__ == '__main__':
    run()

