#!/usr/bin/python
import requests
import json

server_url = "housedroid-v1-0.appspot.com"

class iplink():
  def __init__(self, url = server_url):
    self.url = url

  def post(self, message, url = "/sendData"):
    url = self.url + url
    response = requests.post(url, data = json.dumps(message), headers = {"content-type": "application/json"})

  def get(self, url = "/getData"):
    url = self.url + url
    response = requests.get(url)
    return response.json()
