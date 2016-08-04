# -*- coding: utf-8 -*-
from flask import Flask, jsonify, request
from base import ApiClient, Handler

app = Flask(__name__)

from handlers.currency import currency
from handlers.weather import weather

app.route('/currency', methods=['GET', 'POST'])(currency)
app.route('/weather', methods=['GET', 'POST'])(weather)