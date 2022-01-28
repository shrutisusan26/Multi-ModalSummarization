from cgi import test
import json
from fastapi.testclient import TestClient
from geteval import  test_text
from baas_api import app
import re
client = TestClient(app)

localhost="http://127.0.0.1:8000/"

with open(r'.\Eval\Dataset\newsroom-release\release\test-stats.jsonl', 'r') as json_file:
    json_list = list(json_file)

pred_sents,ref_sents=[],[]
for json_str in json_list:
    result = json.loads(json_str)  
    if result['density_bin']=='extractive':
        print(result['text'])
        sents=  re.split(r'[?.]',result['text'])[:-1]
        dictionary={}
        for i,sent in enumerate(sents):
                print(sent)
                dictionary[str(i)]=re.sub('"','',sent.strip())
        print(dictionary)         
        summary_id=client.post(localhost+"summary",json={"article":dictionary ,"t_clusters":2,'fpath':"result\\result","order": {}})
        print(summary_id,summary_id.status_code,summary_id.text)
        assert summary_id.status_code == 201
        summary_id=summary_id.json()
        
        text_sum_order= client.get(localhost+f"tresult/{str(summary_id)}")
        assert text_sum_order.status_code == 200
        text_sum_order=text_sum_order.json()
        
        pred_sents.append('.'.join(text_sum_order.values()))
        ref_sents.append(result['summary'])
        break
print(pred_sents)
print(ref_sents)

test_text(pred_sents,ref_sents)
