# -*- coding: utf-8 -*-
import urllib
import re
import requests
from datetime import datetime, timedelta
from lxml import etree
from config import ENDPOINT_URL, CURRENCY_API_KEY
from base import Handler, ApiClient


class NBKRClient(object):
    def __init__(self):
        self.last_check = None
        self.currencies = {}
    
    def load_currencies(self):
        response = requests.get('http://www.nbkr.kg/XML/daily.xml')
        tree = etree.XML(response.content)
        currencies = tree.xpath('//Currency')
        for currency in currencies:
            self.currencies[currency.attrib['ISOCode']] = float(currency.find('Value').text.replace(',', '.'))
        self.last_check = datetime.now()
    
    def get(self, currency):
        if not self.last_check or self.last_check < datetime.now() - timedelta(hours=1):
            try:
                self.load_currencies()
            except:
                pass
        if currency.upper().strip() in self.currencies:
            return self.currencies[currency.upper()]
        return ''
    
    def get_all(self):
        if not self.last_check or self.last_check < datetime.now() - timedelta(hours=1):
            try:
                self.load_currencies()
            except:
                pass
        return self.currencies


currency_handler = Handler()
client = ApiClient(CURRENCY_API_KEY, ENDPOINT_URL)
nbkr_client = NBKRClient()

HELP_TEXT = """
Комманды бота:
курс - вывести курс валют(USD, EUR, KZT, RUB)
usd - курс доллара на сегодня
eur - курс евро на сегодня
kzt - курс тенге на сегодня
rub - курс рубля на сегодня
[n] [iso_code] - конвертация валюты в сомы
Пример:
10 KZT
Ответ:
1.1997
"""


@currency_handler.bind('user/follow')
def on_follow(data):
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

@currency_handler.bind('message/new')
def on_message(data):
    data['content'] = urllib.unquote(data['content'])
    if data['content'].lower().strip() == u'курс':
        currencies = nbkr_client.get_all()
        response = client.send_message(data['chat_id'], """
        USD - {0}
        EUR - {1}
        KZT - {2}
        RUB - {3}
        """.format(
            currencies['USD'],
            currencies['EUR'],
            currencies['KZT'],
            currencies['RUB']
        ))
        return {
            'success': response['success']
        }
    result = re.search('(\d+)\s+(KZT|USD|EUR|RUB|kzt|usd|eur|rub)', data['content'])
    if result:
        total = result.group(1)
        currency = result.group(2)
        rate = nbkr_client.get(currency)
        if rate == '':
            return {
                'success': False
            }
        response = client.send_message(data['chat_id'], """
            {0} {1} = {2} som
        """.format(total, currency, rate * float(total)))
        return {
            'success': response['success']
        }
    rate = nbkr_client.get(data['content'])
    if rate == '':
        return {
            'success': False
        }
    response = client.send_message(data['chat_id'], """
    1 {0} = {1} som
    """.format(data['content'], rate))
    return {
        'success': response['success']
    }


def currency():
    return currency_handler.handle()