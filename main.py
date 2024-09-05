from aiogram import Bot, Dispatcher, executor, types
import logging
from downloader import YouTubeVideoDownloader, InstagramDownloader
from os import remove

bot = Bot("7436824817:AAE6g7Ecj-B0HVWT58t_VefKFDMibk4BfMU")
dp = Dispatcher(bot)

@dp.message_handler(commands=['start'])
async def CommandStart(message: types.Message):
    await message.answer(f"Salom {message.from_user.full_name}")

@dp.message_handler()
async def echo(message: types.Message):
    if message.text.startswith("https://youtube.com/") or message.text.startswith("https://www.youtube.com/") or message.text.startswith("https://youtu.be/"):
        await message.answer("Video yuklanmoqda...")

        video = YouTubeVideoDownloader(message.text)

        try:
            with open("video.mp4", "rb") as video_file:
                await message.answer_video(video=video_file, caption=f"Video nomi: {video.get('title')}\nVideo yuklagan shaxs: {video.get('uploader')}\nLayklar soni: {video.get('like_count')}\nDislayklar soni: {video.get('dislike_count')}\nKo'rishlar soni: {video.get('view_count')}\nVideo yuklangan sana: {video.get('upload_date')}")
                await message.answer(f"Video izohi: {video.get('description')}")
        except Exception as e:
            await bot.send_message(chat_id=5230484991, text=f"{e}")

        remove("video.mp4")
    elif message.text.startswith("https://www.instagram.com/") or message.text.startswith("https://instagram.com/"):
        downloaded = InstagramDownloader(message.text)
        try:
            await message.answer_video(video=downloaded['url'])
            await message.answer(downloaded['description'])
        except Exception as e:
            await bot.send_message(chat_id=5230484991, text=f"{e}")


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    executor.start_polling(dp, skip_updates=False)