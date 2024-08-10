import datetime
import webbrowser
from pytube import YouTube, Search

def read_file(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            return file.read()
    except (FileNotFoundError, IOError) as e:
        return None

def extract_cmd_info(response):
    response = response.strip()
    if response.startswith('[GEN]'):
        return None

    if response.startswith("YouTube:"):
        part = response.split("YouTube:")[1].strip()
        return { 'cmd': 'YouTube', 'song_name': part }
    
    if response.startswith("Time"):
        return { 'cmd': 'Time' }
    
    return None

def play_song(query):
    search = Search(query)
    video = search.results[0]  # Get the first search result
    video_url = video.watch_url
    webbrowser.open(video_url)

def get_current_time():
        now = datetime.datetime.now()
        time_str = now.strftime("الوقت الحالي هو %I:%M %p")
        return time_str
