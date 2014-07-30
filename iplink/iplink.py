#!/usr/bin/python
import requests
import json

# Mushed <sender.py> and <receiver.py> together

class iplink():
    def __init__(self, url = "http://127.0.0.1:3000"):
        self.url = url

    def post(self, message, url = "/submitdata"):
        url = self.url + url
        response = requests.post(url, data = json.dumps(message), headers = {"content-type": "application/json"})

    def get(self, url = "/getdata"):
        url = self.url + url
        response = requests.get(url)
        return response.json()
