#!/usr/bin/python
import requests

# Mushed <sender.py> and <receiver.py> together

class iplink():
    def __init__(self, url = "http://127.0.0.1:3000"):
        self.url = url

    def post(self, data, extraurl = "/submitdata"):
        url = self.url + extraurl
		response = requests.post(url, data)

    def get(self, extraurl = "/getdata"):
        url = self.url + extraurl
		response = requests.get(url)
		return response.text
