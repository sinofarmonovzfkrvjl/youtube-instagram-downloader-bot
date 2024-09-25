# main.py

from fastapi import FastAPI, Request
from aiogram.types import Update
from main import dp, bot  # Import dispatcher and bot from bot.py
from config import WEBHOOK_URL
import logging

# Initialize logging
logging.basicConfig(level=logging.INFO)

# FastAPI app initialization
app = FastAPI()

# FastAPI startup event to set the webhook
@app.on_event("startup")
async def on_startup():
    await bot.set_webhook(WEBHOOK_URL)
    logging.info(f"Webhook set to {WEBHOOK_URL}")

# FastAPI shutdown event to delete the webhook
@app.on_event("shutdown")
async def on_shutdown():
    await bot.delete_webhook()
    logging.info("Webhook deleted")

# Aiogram webhook handler for FastAPI
@app.post("/webhook")
async def process_webhook(request: Request):
    update = Update(**await request.json())
    await dp.feed_update(bot, update)
    return {"status": "ok"}

if __name__ == "__main__":
    import uvicorn
    # Run FastAPI with uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
