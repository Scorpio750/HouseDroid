from urllib2 import *

try :
	connection = urlopen("http://127.0.0.1:3000/getdata")
	data = connection.read()
	print data

except:
	print reason
