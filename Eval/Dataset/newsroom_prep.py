from cgi import test
import json
from fastapi.testclient import TestClient
from Eval.geteval import  test_text
from baas_api import app

client = TestClient(app)

localhost="http://127.0.0.1:8000/"

with open('./newsroom-release/test-stats.jsonl', 'r') as json_file:
    json_list = list(json_file)

pred_sents,ref_sents=[],[]
for json_str in json_list:
    result = json.loads(json_str)
    if result['density_bin']=='extractive':

        client.post(localhost+"summary",json={"article": result['article'],"t_clusters":response['t_clusters'],"order": {}})
        
        assert summary_id.status_code == 201
        summary_id=summary_id.json()
        
        text_sum_order= client.get(localhost+f"tresult/{str(summary_id)}")
        assert text_sum_order.status_code == 200
        text_sum_order=text_sum_order.json()
        
        pred_sents.append(text_sum_order.values())
        ref_sents.append(result['summary'].split('.'))


test_text(pred_sents,ref_sents)
