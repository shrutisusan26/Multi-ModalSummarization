from cgitb import text
from report_gen import  report_gen
from final_summary import combine_summaries
from fastapi.testclient import TestClient
from baas_api import app
import os
from Transcription.process_transcript import process_yttranscript
import json

client = TestClient(app)
localhost="http://127.0.0.1:8000/"
path= r"E:\Multi-Modal Summarization\Data\videos"
paths=['econ.mp4' ]
for videos in paths:
    req=client.post(localhost+"getfrompath/",params={'path':os.path.join(path,videos)})
    assert req.status_code == 200
    response=req.json()

    #print(response['transcript'])

    url = "https://www.youtube.com/watch?v=j5XdY5wkVTA&list=PLUl4u3cNGP63Z979ri_UXXk_1zrvrF77Q"
    #print(url)
    req=client.post(localhost+"link",json={"url":url})
    #print(req.status_code)
    assert req.status_code == 201
    response1=req.json()

    #print(response1)
    with open(response1) as json_file:
        transcript = json.load(json_file)
    print(process_yttranscript(transcript))
    summary_id= client.post(localhost+"summary",json={"article": process_yttranscript(transcript),"t_clusters":response['t_clusters'],"fpath":os.path.join(path,videos),"order": {}})
    assert summary_id.status_code == 201
    summary_id=summary_id.json()
    text_sum_order= client.get(localhost+f"tresult/{str(summary_id)}")
    assert text_sum_order.status_code == 200
    text_sum_order=text_sum_order.json()

    vsummary_id=  client.post(localhost+"vsummary",json={"path": response['dpath'],"v_clusters": response['v_clusters'],"order": [0],"fr":0,"t_chunks": 0})
    assert vsummary_id.status_code == 201
    vsummary_id=vsummary_id.json()

    video_sum_order= client.get(localhost+f"vresult/{str(vsummary_id)}")
    assert video_sum_order.status_code == 200
    video_sum_order=video_sum_order.json()

    report_dic =  combine_summaries(text_sum_order,video_sum_order['order'],video_sum_order['fr'],video_sum_order['t_chunks'])
    report_gen(report_dic,os.path.join(path,videos),video_sum_order['fr'])
    print("report generated")