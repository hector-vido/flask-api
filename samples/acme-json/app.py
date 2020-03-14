#!/usr/bin/env python3

from os import environ
from pymongo import MongoClient
from flask import Flask, jsonify

app = Flask(__name__)

client = MongoClient('mongodb://{0}:{1}@{2}:27017/admin'.format(environ['MONGO_USER'], environ['MONGO_PASS'], environ['MONGO_HOST']))
db = client.acme

@app.route('/')
def home():
    return jsonify([u for u in db.usuarios.find()])

app.run(host='0.0.0.0', port=5000, debug=True)
