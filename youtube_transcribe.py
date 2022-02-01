from  youtube_transcript_api import YouTubeTranscriptApi
import json
import os
from helper import dirgetcheck

def get_yt_transcript(url):
    try:
        _id = url.split("=")[1].split("&")[0]
        print(_id)
    except:
        print("Invalid link")
    
    transcripts = YouTubeTranscriptApi.get_transcripts([_id])
    print(transcripts)
    sentences={}
    dir = dirgetcheck('Data','trans')
    for sent in transcripts[0][_id]:
        sentences[sent['start']]=sent['text']
    with open(os.path.join(dir,f'{_id}.json'), 'w', encoding='utf-8') as json_file:
            json.dump(sentences, json_file)
    return os.path.join(dir,f'{_id}.json')
            
if __name__=="__main__":
    example_url = "https://www.youtube.com/watch?v=qLvwlsCjMfY&ab_channel=TheMysticaLand"
    get_yt_transcript(example_url)