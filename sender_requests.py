import requests

payload = {'data':'5'}

# create a response object using the requests library
response = requests.post('http://127.0.0.1:3000/submitdata', data=payload)
print response.text
