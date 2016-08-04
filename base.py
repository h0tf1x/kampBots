# -*- coding: utf-8 -*-
from flask import jsonify, request
import requests

class Handler(object):

    def __init__(self):
        self.handlers = {}
        pass
        
    def bind(self, event):
        def decorator(f):
            self.handlers[event] = f
        return decorator
    
    def handle(self):
        print "Handle"
        print request.json
        if not request.json:
            print "not json request"
            return jsonify({
                'success': False,
            }) 
        data = request.json
        print data
        if data['event'] in self.handlers:
            return jsonify(self.handlers[data['event']](data['data']))
        return jsonify({
            'success': False,
            'message': 'Handler not bound'
        })


class ApiClient(object):
    
    def __init__(self, api_key, endpoint_url='http://api.kamp.kg'):
        self.endpoint_url = endpoint_url
        self.api_key = api_key
    
    def get_headers(self):
        return {
            'X-Namba-Auth-Token': self.api_key 
        }
    
    def post(self, url, data):
        response = requests.post(url, data=data, headers=self.get_headers())
        return response.json()
    
    def create_chat(self, user_id):
        return self.post(self.endpoint_url + '/chats/create', {
            'name': '',
            'image': '',
            'is_private': 0,
            'members': [user_id]
        })
        
    def send_message(self, chat_id, message):
        return self.post(self.endpoint_url + '/chats/' + str(chat_id) + '/write', {
            'type': 'text/plain',
            'content': message
        })