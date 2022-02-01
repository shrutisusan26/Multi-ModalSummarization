from fastapi import FastAPI, status ,HTTPException, File, UploadFile
import shutil
import os
from fastapi.responses import JSONResponse
from bson.objectid import ObjectId
from TextSummarization.tclustering import gen_summary
from VideoSummarization.vclustering import vsum
from entities.apimodels import Article,Vidpath,Transcript
from entities.dbschemas import summaryEntity,vsummaryEntity
from Transcription.videofuncs import getmd, upload, getdir
from VideoSummarization.url_downloader import download_url
from helper import calc_clusters,dirgetcheck
from bson import json_util
import json
from fastapi.middleware.cors import CORSMiddleware
from config.db import conn, start
from Transcription.youtube_transcribe import get_yt_transcript
from typing import  Optional
db = conn.Vidsum
start()
def parse_json(data):
    return json.loads(json_util.dumps(data))

tags_metadata = [
    {
        "name": "upload_video",
        "description": "Returns the transcript generated from the video with optimal number of text and video clusters determined",
    },
    {
        "name": "video_summary",
        "description": "Returns the _id of the extracted key frames after insertion into the database",
    },
    {
        "name": "link",
        "description": "API for extracting transcript from youtube videos with URLs ",
    },
    {
        "name": "text_summary",
        "description": "Determines the key sentences from the transcript and returns the _id of its entry in database",
    },
    {
        "name": "video_order",
        "description": "Returns the ordering of keyframes extracted after retrieving from database",
    },
    {
        "name": "text_order",
        "description": "Returns the ordering of keysentences extracted after retrieving from database"    }
    
]
    
app = FastAPI(openapi_tags=tags_metadata)
origins = [
    "http://localhost:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/uploadfile/",tags=["upload_video"])
async def create_upload_file(file: UploadFile = File(...)):
    dir = getdir(file)
    if dir == 'Invalid':
        return {"message": "Filetype not supported"}
    destination = os.path.join(dir,file.filename)
    try:
        with open(destination,"wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
    finally:
        transcription = upload(destination,db)
        duration, ofps = getmd(destination)
        v_clusters,t_clusters = calc_clusters(duration,ofps)
        file.file.close()
    return {"transcript": transcription, "dpath":destination, 'v_clusters':v_clusters, 't_clusters':t_clusters}

@app.post("/vsummary", response_description="Post path for video summary",tags=["video_summary"])
async def vsummary(path: Vidpath):
    path = path.dict()
    if( db_path := db.Vimage.find_one({"path": path}) ) is not None:
        return JSONResponse(status_code=status.HTTP_201_CREATED, content=parse_json(db_path)['_id']['$oid'])
    ordering,fr,t_chunks = vsum(path['path'],path['v_clusters'])
    item={'path':path,'order':ordering,'fr':fr,'t_chunks':t_chunks}
    response =  db.Vimage.insert_one(vsummaryEntity(item))
    item['id']= str(response.inserted_id)
    return JSONResponse(status_code=status.HTTP_201_CREATED, content=item['id'])

@app.post("/summary", response_description="Post article for summary",tags=["text_summary"])
async def summary(article:Article):
    article = article.dict()
    if( article_db := db.Article.find_one({"article": article['article']}) ) is not None:
        return JSONResponse(status_code=status.HTTP_201_CREATED, content=parse_json(article_db)['_id']['$oid'])
    ordering = gen_summary(article['article'],article['fpath'],article['t_clusters'])
    item={'article':article['article'],'order':ordering}
    response =  db.Article.insert_one(summaryEntity(item))
    item['id']= str(response.inserted_id)
    return JSONResponse(status_code=status.HTTP_201_CREATED, content=item['id'])

@app.post("/link", response_description="To pass the link to a youtube video",response_model=dict,tags=["link"])
async def transcript_post(link:Transcript):
    link = link.dict()
    dir=dirgetcheck('Data','videos')
    destination=download_url(link['url'],dir)
    print(destination)
    try: 
        transcription = get_yt_transcript(link['url'])
    except:
        transcription = upload(destination,db)
    duration, ofps = getmd(destination)
    v_clusters,t_clusters = calc_clusters(duration,ofps)
    return {"transcript": transcription, "dpath":destination, 'v_clusters':v_clusters, 't_clusters':t_clusters}

@app.get('/tresult/{id}',response_description="Retrieves the summary", response_model=dict,tags=["text_order"])
async def tresult(id:str):
   if( article := db.Article.find_one({"_id": ObjectId(id)}) ) is not None:
        return article['order']
   raise HTTPException(status_code=404, detail=f"Article {id} not found")

@app.get('/vresult/{id}',response_description="Retrieves the video images", response_model=dict,tags=["video_order"])
async def vresult(id:str):
   if( path := db.Vimage.find_one({"_id": ObjectId(id)}) ) is not None:
        dictionary={'order':path['order'],'fr':path['fr'],'t_chunks':path['t_chunks']}
        return dictionary
   raise HTTPException(status_code=404, detail=f"Vimages {id} not found")