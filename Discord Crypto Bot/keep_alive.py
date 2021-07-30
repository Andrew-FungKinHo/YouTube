from flask import Flask
from threading import Thread 

app = Flask('')

@app.route('/')
def home():
  return 'Hello. The Crypto Bot is running YA YEET!'

def run():
  app.run(host='0.0.0.0',port=8000)

def keep_alive():
  t = Thread(target=run)
  t.start()