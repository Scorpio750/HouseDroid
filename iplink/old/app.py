from flask import Flask, request

app = Flask(__name__)
data = {}

@app.route('/')
def display():
	return str(data)

@app.route('/submitdata', methods = ['POST'])
def submit():
	data = request.json

@app.route('/getdata', methods = ['GET'])
def send():
	data = request.json

if __name__ == '__main__':
	app.run('127.0.0.1', port=3000, debug=True)
