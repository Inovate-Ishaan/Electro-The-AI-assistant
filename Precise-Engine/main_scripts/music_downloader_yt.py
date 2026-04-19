from youtube_search import YoutubeSearch
from yt_dlp import YoutubeDL
import soundfile as sf
yt_opts = {#"extract_audio" : True,
            "format" : "bestaudio/best",
            "outtmpl" : "music",
            "postprocessors" : [{
                'key' : 'FFmpegExtractAudio',
                'preferredcodec' : 'wav',
                'preferredquality' : '360',
            }],
            'noplaylist' : True,
            'ignoreerrors' : True,
            'quiet' : True,  #to suppress console output
            }

def get_music(query):
    try:
        result = YoutubeSearch(query, max_results=1).to_dict()
        url = "https://youtube.com" + result[0]["url_suffix"]
        title = result[0]["title"]
        audio = YoutubeDL(yt_opts).download(url)
        return True, title
    except:
        return False

if __name__ == "__main__":
    get_music("Bezubaan")
    pass