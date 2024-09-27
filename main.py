import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.types import FSInputFile
from aiogram.filters import CommandStart
import logging
from downloader import YouTubeVideoDownloader, InstagramDownloader
import glob
from os import remove
import requests
from aiogram.webhook.aiohttp_server import SimpleRequestHandler

dp = Dispatcher()

@dp.message(CommandStart())
async def command_start(message: types.Message):
    await message.answer(f"Salom {message.from_user.full_name}\nmen youtube va instagramdan video yuklovchi botman")

@dp.message()
async def echo(message: types.Message):
    if message.text.startswith(("https://youtube.com/", "https://www.youtube.com/", "https://youtu.be/", "https://tiktok.com/", "https://www.tiktok.com/", "https://www.facebook.com/", "https://www.facebook.com")):
        await message.answer("Video yuklanmoqda...")
        video = YouTubeVideoDownloader(message.text)
        try:
            if video:
                video_file = FSInputFile(glob.glob("*.mp4")[0])
                await message.answer_video(
                    video=video_file,
                    caption=f"Video nomi: {video.get('title')}\n"
                            f"Video yuklagan shaxs: {video.get('uploader')}\n"
                            f"Layklar soni: {video.get('like_count')}\n"
                            f"Dislayklar soni: {video.get('dislike_count')}\n"
                            f"Ko'rishlar soni: {video.get('view_count')}\n"
                            f"Video yuklangan sana: {video.get('upload_date')}"
                )
                await message.answer(f"Video izohi: {video.get('description')}")
            else:
                await message.answer("Video yuklayolmadim")
        except:
            pass
        remove(glob.glob("*.mp4")[0])
    elif message.text.startswith(("https://www.instagram.com/", "https://instagram.com/")):
        await message.answer("Video yuklanmoqda")
        downloaded = InstagramDownloader(message.text)
        response = requests.get(downloaded['url'])
        if message.text.startswith("https://www.instagram.com/p/"):
            with open("image.png", "wb") as f:
                f.write(response.content)
            try:
                await message.answer_photo(FSInputFile("image.png"))
                await message.answer(str(downloaded['description']))
            except Exception as e:
                await message.answer(e)
            remove("image.png")
        elif message.text.startswith("https://www.instagram.com/reel/"):
            with open('video.mp4', 'wb') as f:
                f.write(response.content)
            try:
                await message.answer_video(types.FSInputFile("video.mp4"))
                await message.answer(str(downloaded['description']))
            except Exception as e:
                await message.answer("Videoni yuklab bo'lmadi")
            remove("video.mp4")

async def main():
    API_TOKEN = "7307034091:AAFA4FWLTii3n3eONLDswwY7StXey1mlM0A"
    bot = Bot(API_TOKEN)
    await dp.start_polling(bot, polling_timeout=False)

if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    asyncio.run(main())