#!/usr/bin/python
import urllib, urllib2

# Mushed <sender.py> and <receiver.py> together

class iplink():
    def __init__(self, url):
        self.url = url

    def post(self, data, extraurl = ""):
        url = self.url + extraurl
        encoded = urllib.urlencode(data)
        request = urllib2.Request(url, encoded)
        try:
            response = urllib2.urlopen(request)
            return response
        except urllib2.URLError, e:
            print e.reason
            return None

    def get(self, extraurl = ""):
        url = self.url + extraurl
        try:
            response = urllib2.urlopen(url)
            return response.read()
        except urllib2.URLError, e:
            print e.reason
            return None

