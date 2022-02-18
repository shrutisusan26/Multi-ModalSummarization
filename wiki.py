from cgi import test
import json
from fastapi.testclient import TestClient
from Eval.text_eval.geteval import  test_text
from baas_api import app
import re
import os
import csv
import pickle

client = TestClient(app)
# pred_sents,ref_sents=[],[]
# with open("refs.pkl","rb") as rf:
#     ref_sents = pickle.load(rf)
# with open("pred.pkl","rb") as pf:
#     pred_sents = pickle.load(pf)
# print(len(pred_sents))
# print(len(ref_sents))
# test_text(pred_sents,ref_sents)
localhost="http://127.0.0.1:8000/"

dir1 = r'E:\Multi-Modal Summarization\Eval\Dataset\Wikihow\ActualWH'
dir2 = r'E:\Multi-Modal Summarization\Eval\Dataset\Wikihow\SummaryWH'
text_list = os.listdir(dir1)
new_dict =[]
pred_sents,ref_sents=[],[]
idx=0
for fname in text_list[:5000]:
    try:
        d ={}
        with open(os.path.join(dir1,fname),"r",encoding ='utf8') as f:
            text = f.readlines()
        dictionary={}
        for i,sent in enumerate(text):
                #print(sent)
                dictionary[str(i)]=text[i]
        #print(dictionary)       
        summary_id=client.post(localhost+"summary",json={"article":dictionary ,"t_clusters":3,'fpath':"result\\result","order": {}})
        #print(summary_id,summary_id.status_code,summary_id.text)
        assert summary_id.status_code == 201
        summary_id=summary_id.json()
        text_sum_order= client.get(localhost+f"tresult/{str(summary_id)}")
        assert text_sum_order.status_code == 200
        text_sum_order=text_sum_order.json()
        
        with open(os.path.join(dir2,fname),"r",encoding ='utf8') as f:
            summ = f.read()
        if summ!='' and len(text_sum_order.values())>0:
            pred_sents.append('.'.join(text_sum_order.values()))
            ref_sents.append(str(summ))
            d['ref']=summ
            d['pred']='.'.join(text_sum_order.values())
            #break
            new_dict.append(d)
    except Exception as e:
        print(e)
        continue
    finally:
        idx+=1
        if idx%100==0:
            print(idx,len(pred_sents),len(ref_sents))
with open("refs.pkl","wb") as rf:
    pickle.dump(ref_sents,rf)
with open("pred.pkl","wb") as pf:
    pickle.dump(pred_sents,pf)
test_text(pred_sents,ref_sents)
with open('all.csv', 'w',encoding='utf8') as csvfile:
    try:
        writer = csv.DictWriter(csvfile, fieldnames = ['ref','pred'])
        writer.writeheader()
        writer.writerows(new_dict)
    except:
        pass
