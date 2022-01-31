from cgitb import text
from report_gen import  report_gen
from sync import combine_summaries
from fastapi.testclient import TestClient
from baas_api import app
import os
from Transcription.process_transcript import process_yttranscript

client = TestClient(app)
localhost="http://127.0.0.1:8000/"
path= r"E:\Multi-Modal Summarization\Data\videos"
paths=['econ.mp4' ]
for videos in paths:


    url = "https://www.youtube.com/watch?v=xyAuNHPsq-g&ab_channel=KhanAcademy"
    req=client.post(localhost+"link",json={"url":url})
    assert req.status_code == 201
    response=req.json()

    summary_id= client.post(localhost+"summary",json={"article": response['transcript'],"t_clusters":response['t_clusters'],"fpath":response['dpath'],"order": {}})
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
    report_gen(report_dic,response['dpath'],video_sum_order['fr'])
    print("report generated")