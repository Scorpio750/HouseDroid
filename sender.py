#! /usr/bin/python

import urllib, urllib2

# string to hold URL
url = "http://127.0.0.1:3000/submitdata"

# place POST data in a dictionary
# post_data_dictionary = {'data':5}

# encode POST data to be sent into a URL
# post_data_encoded = urllib.urlencode(post_data_dictionary)

# make a request object to hold POST data and URL
# request_object = urllib2.Request(url, data=post_data_encoded)

# make the request using request object as argument, store response in a variable
try:
	response = urllib2.urlopen(url,data="5")
	print response.read()
except urllib2.URLError,e:
	print e.reason
