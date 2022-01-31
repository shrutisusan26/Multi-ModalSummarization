from  youtube_transcript_api import YouTubeTranscriptApi
from fastapi.testclient import TestClient
import json
from baas_api  import app
import re
client = TestClient(app)

localhost="http://127.0.0.1:8000/"
def procyt(sentence):
    sentences = {}
    ts = list(sentence.keys())
    sent = list(sentence.values())
    for i in range(len(sent)):
        sent[i]=re.sub('\[(.*?)\]','',sent[i])
        if sent[i]!='':
            sent[i]=re.sub('\n+',' ',sent[i]).strip()
            if sent[i][-1] in ['.','!','?']:
                sentences[ts[i]]=sent[i]
            else:
                flag = 0
                j = i+1
                asent = ''
                while flag!=1:
                    sent[j]=re.sub('\n+',' ',sent[j]).strip()
                    if( re.search(r'[.?!]', sent[j])):
                        index= re.search(r'[.?!]', sent[j]).end()
                        print(index)
                        sent=''.join(list(sent[j][:int(index)]))
                        flag=1
                        asent=asent+' ' + sent
                        sent=''.join(list(sent[j][int(index):]))
                        sent[j]=''
                        sent[j]=sent
                    else:
                        asent= asent + ' ' + sent[j]
                        sent[j]=''
                        j=j+1
                sentences[ts[i]]=sent[i]+asent
        else:
            continue
    #print(sentences)
    return sentences 

example_url = "https://www.youtube.com/watch?v=j5XdY5wkVTA&list=PLUl4u3cNGP63Z979ri_UXXk_1zrvrF77Q"
_id = example_url.split("=")[1].split("&")[0]
print(_id)

transcripts = YouTubeTranscriptApi.get_transcripts([_id])
sentences={}
for sent in transcripts[0][_id]:
    sentences[sent['start']]=sent['text']
sentence= procyt(sentences)
print(sentence)
summary_id=client.post(localhost+"summary",json={"article":sentence ,"t_clusters":len(sentence)/3,'fpath':"result\\result","order": {}})
print(summary_id,summary_id.status_code,summary_id.text)
assert summary_id.status_code == 201
summary_id=summary_id.json()
with open(f'./Transcription/yt_transcripts/{_id}.json', 'w', encoding='utf-8') as json_file:
        json.dump(sentence, json_file)