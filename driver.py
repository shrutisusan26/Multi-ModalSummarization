from cgitb import text
from report_gen import  report_gen
from sync import combine_summaries
from fastapi.testclient import TestClient
from baas_api import app
import os
from Transcription.process_transcript import readj

client = TestClient(app)
localhost="http://127.0.0.1:8000/"
path= r"E:\Multi-Modal Summarization\Data\videos"
paths=['fc.mp4' ]
for videos in paths:


    # url = "https://rr2---sn-o097znss.googlevideo.com/videoplayback?expire=1643757030&ei=hmn5YbHyBeeK6dsP0Paq0AY&ip=154.22.132.165&id=o-AF7J1H5LeejRa36ToHUb0tGHm4Jho1iGSmCjcfM8xbjy&itag=18&source=youtube&requiressl=yes&mh=yn&mm=31%2C29&mn=sn-o097znss%2Csn-5hne6nsr&ms=au%2Crdu&mv=m&mvi=2&pl=23&initcwndbps=963750&vprv=1&mime=video%2Fmp4&gir=yes&clen=11535965&ratebypass=yes&dur=710.646&lmt=1541083293866002&mt=1643735093&fvip=2&fexp=24001373%2C24007246&c=ANDROID&txp=5431432&sparams=expire%2Cei%2Cip%2Cid%2Citag%2Csource%2Crequiressl%2Cvprv%2Cmime%2Cgir%2Cclen%2Cratebypass%2Cdur%2Clmt&sig=AOq0QJ8wRQIhAK9xJoQd_K-vOtvnz5i_qzujc_-SYMvL78TKjeFz8FhAAiBpBv6DDp7zAc_6h6GFJF3pbdU9hNhuBD-ziLfzthilXg%3D%3D&lsparams=mh%2Cmm%2Cmn%2Cms%2Cmv%2Cmvi%2Cpl%2Cinitcwndbps&lsig=AG3C_xAwRgIhAPfDREss1Z_DHzdtf7eYHUhKgwcfvUAfheNUlIO7pwepAiEAtqhhW6NoXw3gN18js66KPjbNBpu8FIAbXP51qIdgXvE%3D&title=Y2Mate.is%20-%20Introduction%20to%20matrices-xyAuNHPsq-g-240p-1643735431166"
    # req=client.post(localhost+"link",json={"url":url})
    # assert req.status_code == 201
    # response=req.json()
    transcr = r'E:\Multi-Modal Summarization\Data\trans\edd60f58-2f89-42be-abb2-8b89ef99f166result.json'

    summary_id= client.post(localhost+"summary",json={"article": readj(transcr),"t_clusters":20,"fpath":os.path.join(path,videos),"order": {}})
    assert summary_id.status_code == 201
    summary_id=summary_id.json()

    text_sum_order= client.get(localhost+f"tresult/{str(summary_id)}")
    assert text_sum_order.status_code == 200
    text_sum_order=text_sum_order.json()

    vsummary_id=  client.post(localhost+"vsummary",json={"path": os.path.join(path,videos),"v_clusters": 10,"order": [0],"fr":0,"t_chunks": 0})
    assert vsummary_id.status_code == 201
    vsummary_id=vsummary_id.json()

    video_sum_order= client.get(localhost+f"vresult/{str(vsummary_id)}")
    assert video_sum_order.status_code == 200
    video_sum_order=video_sum_order.json()

    report_dic =  combine_summaries(text_sum_order,video_sum_order['order'],video_sum_order['fr'],video_sum_order['t_chunks'])
    report_gen(report_dic,os.path.join(path,videos),video_sum_order['fr'])
    print("report generated")