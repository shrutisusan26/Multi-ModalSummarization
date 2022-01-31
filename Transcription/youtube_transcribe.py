from  youtube_transcript_api import YouTubeTranscriptApi
import json
 

def get_yt_transcript(url):
    try:
        _id = url.split("=")[1].split("&")[0]
        print(_id)
    except:
        print("Invalid link")

    transcripts = YouTubeTranscriptApi.get_transcripts([_id])
    sentences={}
    for sent in transcripts[0][_id]:
        sentences[sent['start']]=sent['text']
    with open(f'{_id}.json', 'w', encoding='utf-8') as json_file:
            json.dump(sentences, json_file)
    return f'{_id}.json'
            
if __name__=="__main__":
    example_url = "https://www.youtube.com/watch?v=pN3jRihVpGk&list=PLKiU8vyKB6ti1_rUlpZJFdPaxT04sUIoV&index=1"
    get_yt_transcript(example_url)