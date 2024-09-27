from flask import Flask
from threading import Thread

app = Flask(__name__)

@app.route("/")
def home():
    try:
        return "Alive"
    except:
        return "Not Alive"

def run():
    app.run(host="0.0.0.0", port=8080)

def keep_alive():
    t = Thread(target=run)
    t.start()