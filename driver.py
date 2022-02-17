from cgitb import text
from report_gen import  report_gen
from sync import combine_summaries
from fastapi.testclient import TestClient
from baas_api import app
import os
from Transcription.process_transcript import process_yttranscript, readj
import json

client = TestClient(app)
localhost="http://127.0.0.1:8000/"
path= r"E:\Multi-Modal Summarization\Data\videos"
tpath = r"E:\Multi-Modal Summarization\Data\trans"
#paths=['Intro.mp4','History.mp4','Imageform.mp4','Imagerepn.mp4','LinearFilt.mp4','Imagefreq.mp4','Imagesampl.mp4','Edgedet.mp4','Fromedge.mp4','Scalespaces.mp4','lec11.mp4','lec13.mp4','lec14.mp4','lec16.mp4','lec19.mp4','lec22.mp4','lec25.mp4','lec28.mp4','lec31.mp4','lec34.mp4','lec37.mp4','lec40.mp4','lec43.mp4','lec44.mp4' ]
paths = ["ml.mp4"]
for i in range (len(paths)):
    videos = paths[i]

    # url = "https://www.youtube.com/watch?v=rfAvjCf1_ZI&list=PLyqSpQzTE6M_PI-rIz4O1jEgffhJU9GgG"
    # req=client.post(localhost+"link",json={"url":url})
    # assert req.status_code == 201
    # response=req.json()
    fname= videos[:-4]+'.json'
    trans = os.path.join(tpath,fname)
    with open(trans,"r") as f:
        transcr = json.load(f)
    summary_id= client.post(localhost+"summary",json={"article": process_yttranscript(transcr),"t_clusters":35,"fpath":os.path.join(path,videos),"order": {}})
    assert summary_id.status_code == 201
    summary_id=summary_id.json()

    text_sum_order= client.get(localhost+f"tresult/{str(summary_id)}")
    assert text_sum_order.status_code == 200
    text_sum_order=text_sum_order.json()

    vsummary_id=  client.post(localhost+"vsummary",json={"path": os.path.join(path,videos),"v_clusters": 25,"order": [0],"fr":0,"t_chunks": 0})
    assert vsummary_id.status_code == 201
    vsummary_id=vsummary_id.json()

    video_sum_order= client.get(localhost+f"vresult/{str(vsummary_id)}")
    assert video_sum_order.status_code == 200
    video_sum_order=video_sum_order.json()

    report_dic =  combine_summaries(text_sum_order,video_sum_order['order'],video_sum_order['fr'],video_sum_order['t_chunks'])
    report_gen(report_dic,os.path.join(path,videos),video_sum_order['fr'])
    print("report generated")