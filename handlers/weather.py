# -*- coding: utf-8 -*-
import urllib
from datetime import datetime, timedelta
import requests
from config import ENDPOINT_URL, WEATHER_API_KEY
from base import Handler, ApiClient


weather_handler = Handler()
client = ApiClient(WEATHER_API_KEY, ENDPOINT_URL)
HELP_TEXT = """
Комманды бота
погода - вывести информацию о погоде на сегодня
"""


@weather_handler.bind('user/follow')
def help(data):
    response = client.create_chat(data['id'])
    if response['success']:
        response = client.send_message(response['data']['id'], HELP_TEXT)
        if response['success'] is not True:
            print response['message']
            return {
                'success': False,
                'message': u'Ошибка при отправке сообщения'
            }
        return {
            'success': True
        }
    else:
        print response['message']
        return {
            'success': False,
            'message': u'Ошибка при создании чата'
        }


@weather_handler.bind('message/new')
def send_info(data):
    data['content'] = urllib.unquote(data['content'])
    if data['content'].lower().strip() == u'погода':
        response = requests.get('http://api.openweathermap.org/data/2.5/weather?q=Bishkek&APPID=6dc20e5a63676ee67d31de7a61849b69&units=metric')
        response = response.json()
        if response['code'] == 200:
            client.send_message(data['chat_id'], """
            Сегодня в Бишкеке:
            {0}
            Температура: {1}C
            """.format(response['weather'][0]['description'], response['main']['temp']))
            return {
                'success': True,
                'message': ''
            }
        else:
            return {
                'success': False,
                'message': u'Ошибка сервера' 
            }
    else:
        return {
            'success': True,
            'message': u''
        }

def weather():
    return weather_handler.handle()