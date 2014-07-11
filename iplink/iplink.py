#!/usr/bin/python
import urllib, urllib2

# Mushed <sender.py> and <receiver.py> together

class iplink():
    def __init__(self, url = "http://127.0.0.1:3000"):
        self.url = url

    def post(self, data, extraurl = "/submitdata"):
        url = self.url + extraurl
        encoded = urllib.urlencode(data)
        request = urllib2.Request(url, encoded)
        try:
            response = urllib2.urlopen(request)
            return response
        except urllib2.URLError, e:
            print e.reason
            return None

    def get(self, extraurl = "/getdata"):
        url = self.url + extraurl
        try:
            response = urllib2.urlopen(url)
            return response.read()
        except urllib2.URLError, e:
            print e.reason
            return None

