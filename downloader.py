import yt_dlp
import requests

def YouTubeVideoDownloader(url, save_path='.'):
    yt_opts = {
        'outtmpl': f'{save_path}/video.mp4',          # yt-dlp best version is 2024.08.01, 2024.08.06
        'format': 'best'
    }
    with yt_dlp.YoutubeDL(yt_opts) as yt:
        yt.download([url])
    return yt.extract_info(url, download=False)


def InstagramDownloader(url):
    res = requests.get("https://instagram-video-downloader-api-h54m.onrender.com/api/v1/download?url=" + url)
    return {"description": res.json()['description'], "url": f"https://instagram-video-downloader-api-h54m.onrender.com{res.json()['url']}"}