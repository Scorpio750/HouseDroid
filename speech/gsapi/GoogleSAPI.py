import requests

url = "https://www.google.com/speech-api/v1/recognize?xjerr=1&client=chromium&lang=en-US"
rate = 16000

# audio files must only be 15 seconds long or less

def speechtotext(audiofilename):
    assert audiofilename.find(".flac") != -1
    audio = open(audiofilename, "rb").read()
    headers = { "Content-Type": "audio/x-flac; rate={0}".format(rate), \
                "User-Agent": "Mozilla/5.0"}
    response = requests.post(url, data=audio, headers=headers)
    return response.text
    
print speechtotext("soundtest.flac")
