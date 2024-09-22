import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.types import FSInputFile
from aiogram.filters import CommandStart
import logging
from downloader import YouTubeVideoDownloader, InstagramDownloader
from os import remove
import requests

dp = Dispatcher()

@dp.message(CommandStart())
async def command_start(message: types.Message):
    await message.answer(f"Salom {message.from_user.full_name}\nmen youtube va instagramdan video yuklovchi botman")

@dp.message()
async def echo(message: types.Message):
    if message.text.startswith(("https://youtube.com/", "https://www.youtube.com/", "https://youtu.be/")):
        await message.answer("Video yuklanmoqda...")
        video = YouTubeVideoDownloader(message.text)
        video_file = FSInputFile("video.mp4")
        try:
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
        except Exception as e:
            await message.answer(e)
        remove("video.mp4")
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

    bot = Bot(token="7436824817:AAE6g7Ecj-B0HVWT58t_VefKFDMibk4BfMU")
    await dp.start_polling(bot, polling_timeout=False)

if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    asyncio.run(main())