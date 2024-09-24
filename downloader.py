import yt_dlp
import requests

def YouTubeVideoDownloader(url, save_path='.'):
    try:
        yt_opts = {
            'outtmpl': f'{save_path}/video.mp4'          # yt-dlp best version is 2024.08.01, 2024.08.06
        }
        with yt_dlp.YoutubeDL(yt_opts) as yt:
            yt.download([url])
    except:
        return False
    return yt.extract_info(url, download=False)

def InstagramDownloader(url):
    res = requests.get(" https://instagram-video-downloader-api-8voc.onrender.com/api/v1/download?url=" + url)
    return {"description": res.json()['description'], "url": f" https://instagram-video-downloader-api-8voc.onrender.com{res.json()['url']}"}