from flask import Flask, request

app = Flask(__name__)
data = None

@app.route('/')
def display():
	return str(data)

@app.route('/submitdata', methods=['POST'])
def submit():
	global data
<<<<<<< HEAD:app.py
	print "TRYING TO RECEIVE: " + str(request.args)	
	data = request.args
=======
	print "TRYING TO RECEIVE: " + str(request.data)	
	data = request.form['data']
>>>>>>> efeacf0b5865f35193e117f9e51d4a91b10924c2:iplink/app.py
	print "RECEIVED: " + str(data)
	return "RECEIVED: " + str(request)

@app.route('/getdata',methods=['GET'])
def send():
	global data
	return data

if __name__ == '__main__':
	app.run('127.0.0.1', port=3000, debug=True)
