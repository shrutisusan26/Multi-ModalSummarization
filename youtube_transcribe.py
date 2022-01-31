from  youtube_transcript_api import YouTubeTranscriptApi
from fastapi.testclient import TestClient
import json
from baas_api  import app
import re
client = TestClient(app)

localhost="http://127.0.0.1:8000/"
def process_transcript(transcript):
    curr_sentence = []
    processed = {}
    flag = 1
    curr_time = list(transcript.keys())[0]
    for time,sent in transcript.items():
        sent=re.sub('\[(.*?)\]','',sent)
        sent=re.sub('\n+',' ',sent)
        sent = sent.split()
        for i in sent:
            if i[-1] in ['.','?','!']:
                curr_sentence.append(i)
                processed[curr_time] = " ".join(curr_sentence)
                flag = 0
                curr_sentence = []
            else:
                if flag==0:
                    curr_sentence.append(i)
                    continue
                curr_sentence.append(i)
                flag = 1
        if flag==0:
            curr_time = time
    return processed
urls = ["https://www.youtube.com/watch?v=j5XdY5wkVTA&list=PLUl4u3cNGP63Z979ri_UXXk_1zrvrF77Q", "https://www.youtube.com/watch?v=T-H4nJQyMig","https://www.youtube.com/watch?v=HXbsVbFAczg","https://www.youtube.com/watch?v=YUbSpI0J9aQ&t=225s"]
for example_url in urls: 
    _id = example_url.split("=")[1].split("&")[0]
    print(_id)

    transcripts = YouTubeTranscriptApi.get_transcripts([_id])
    sentences={}
    for sent in transcripts[0][_id]:
        sentences[sent['start']]=sent['text']
    sentence= process_transcript(sentences)
    print(sentence)
    summary_id=client.post(localhost+"summary",json={"article":sentence ,"t_clusters":len(sentence)/3,'fpath':"result\\result","order": {}})
    print(summary_id,summary_id.status_code,summary_id.text)
    assert summary_id.status_code == 201
    summary_id=summary_id.json()
    with open(f'./Transcription/yt_transcripts/{_id}.json', 'w', encoding='utf-8') as json_file:
            json.dump(sentence, json_file)