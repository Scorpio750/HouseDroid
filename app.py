#! /usr/bin/python

from flask import Flask, requests

app = Flask(__name__)
data = None

@app.route('/submitdata', methods=['POST'])
def submit():
    global data 
    data = request.args.get('data')

@app.route('/getdata',methods=['GET'])
def send():
    global data
    return data

if __name__ == '__main__':
	app.run()
