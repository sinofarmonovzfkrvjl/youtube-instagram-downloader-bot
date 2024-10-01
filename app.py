from fastapi import FastAPI
from threading import Thread
from fastapi.responses import HTMLResponse

app = FastAPI()

@app.get('/', response_class=HTMLResponse)
async def home():
    return "Alive"

def run():
    import uvicorn
    uvicorn.run(app, host='0.0.0.0', port=8000)

def keep_alive():
    server = Thread(target=run)
    server.start()