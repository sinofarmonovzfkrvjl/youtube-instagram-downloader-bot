from flask import Flask
from threading import Thread

app = Flask(__name__)

@app.get('/')
def home():
    return "Alive"

def run():
    app.run(app, host='0.0.0.0', port=5000)

def keep_alive():
    server = Thread(target=run)
    server.start()