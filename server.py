from fastapi import FastAPI
import threading
import os

app = FastAPI()

def run_bot():    
    os.system("python main.py")

@app.get("/")
async def handle_root():
    thread = threading.Thread(target=run_bot, daemon=True)
    thread.start()
    return {"message": "Bot is running"}
