from cgi import test
import json
from fastapi.testclient import TestClient
from Eval.text_eval.geteval import  test_text
from baas_api import app
import re
import os
import csv

client = TestClient(app)

localhost="http://127.0.0.1:8000/"

dir1 = r'E:\Multi-Modal Summarization\Eval\Dataset\Wikihow\ActualWH'
dir2 = r'E:\Multi-Modal Summarization\Eval\Dataset\Wikihow\SummaryWH'
text_list = os.listdir(dir1)
new_dict =[]
pred_sents,ref_sents=[],[]
for fname in text_list:
    try:
        d ={}
        with open(os.path.join(dir1,fname),"r",encoding ='utf8') as f:
            text = f.readlines()
        dictionary={}
        for i,sent in enumerate(text):
                #print(sent)
                dictionary[str(i)]=text[i]
        #print(dictionary)       
        summary_id=client.post(localhost+"summary",json={"article":dictionary ,"t_clusters":1,'fpath':"result\\result","order": {}})
        print(summary_id,summary_id.status_code,summary_id.text)
        assert summary_id.status_code == 201
        summary_id=summary_id.json()
        
        text_sum_order= client.get(localhost+f"tresult/{str(summary_id)}")
        assert text_sum_order.status_code == 200
        text_sum_order=text_sum_order.json()
        
        pred_sents.append('.'.join(text_sum_order.values()))
        with open(os.path.join(dir2,fname),"r",encoding ='utf8') as f:
            summ = f.read()
        ref_sents.append(summ)
        d['ref']=summ
        d['pred']='.'.join(text_sum_order.values())
        #break
        new_dict.append(d)
    except:
        continue

with open('all.csv', 'w') as csvfile:
    writer = csv.DictWriter(csvfile, fieldnames = ['ref','pred'])
    writer.writeheader()
    writer.writerows(new_dict)
test_text(pred_sents,ref_sents)
