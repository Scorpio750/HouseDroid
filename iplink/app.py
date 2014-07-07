#! /usr/bin/python

from flask import Flask, request

app = Flask(__name__)
data = None

@app.route('/')
def display():
	return str(data)

@app.route('/submitdata', methods=['POST'])
def submit():
	global data
	print "TRYING TO RECEIVE: " + str(request.data)	
	data = request.form['data']
	print "RECEIVED: " + str(data)
	return "RECEIVED: " + str(request)

@app.route('/getdata', methods=['GET'])
def send():
	global data
	return data

if __name__ == '__main__':
	app.run('127.0.0.1', port=3000, debug=True)
