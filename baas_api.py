from fastapi import FastAPI, status ,HTTPException, File, UploadFile
import shutil
import os
import numpy as np
from fastapi.responses import JSONResponse
from bson.objectid import ObjectId
from TextSummarization.tclustering import gen_summary
from VideoSummarization.vclustering import vsum
from models.summary import Article,Vidpath
from schemas.summary import summaryEntity,vsummaryEntity
from Transcription.videofuncs import getmd, upload, getdir
from helper import calc_clusters
from bson import json_util
import json
from fastapi.middleware.cors import CORSMiddleware
from config.db import conn, start

db = conn.Vidsum
start()
def parse_json(data):
    return json.loads(json_util.dumps(data))
app = FastAPI()
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
@app.post("/uploadfile/")
async def create_upload_file(file: UploadFile = File(...)):
    dir = getdir(file)
    print(dir)
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

@app.post("/getfrompath/")
async def create_file(path:str):
    print(path)
    transcription = upload(path,db,upload=False)
    duration, ofps = getmd(path)
    v_clusters,t_clusters = calc_clusters(duration,ofps)
    return {"transcript": transcription, "dpath":path, 'v_clusters':v_clusters, 't_clusters':t_clusters}

@app.post("/vsummary", response_description="Post path for video summary")
async def vsummary(path: Vidpath):
    path = path.dict()
    if( db_path := db.Vimage.find_one({"path": path}) ) is not None:
        return JSONResponse(status_code=status.HTTP_201_CREATED, content=parse_json(db_path)['_id']['$oid'])
    ordering,fr,t_chunks = vsum(path['path'],path['v_clusters'])
    item={'path':path,'order':ordering,'fr':fr,'t_chunks':t_chunks}
    response =  db.Vimage.insert_one(vsummaryEntity(item))
    item['id']= str(response.inserted_id)
    return JSONResponse(status_code=status.HTTP_201_CREATED, content=item['id'])

@app.post("/summary", response_description="Post article for summary")
async def summary(article:Article):
   
    article = article.dict()
    print(article)
    if( article_db := db.Article.find_one({"article": article['article']}) ) is not None:
        return JSONResponse(status_code=status.HTTP_201_CREATED, content=parse_json(article_db)['_id']['$oid'])
    ordering = gen_summary(article['article'],article['t_clusters'])
    item={'article':article['article'],'order':ordering}
    response =  db.Article.insert_one(summaryEntity(item))
    item['id']= str(response.inserted_id)
    return JSONResponse(status_code=status.HTTP_201_CREATED, content=item['id'])

@app.get('/tresult/{id}',response_description="Retrieves the summary", response_model=dict)
async def tresult(id:str):
   if( article := db.Article.find_one({"_id": ObjectId(id)}) ) is not None:
        return article['order']
   raise HTTPException(status_code=404, detail=f"Article {id} not found")

@app.get('/vresult/{id}',response_description="Retrieves the video images", response_model=dict)
async def vresult(id:str):
   if( path := db.Vimage.find_one({"_id": ObjectId(id)}) ) is not None:
        dictionary={'order':path['order'],'fr':path['fr'],'t_chunks':path['t_chunks']}
        return dictionary
   raise HTTPException(status_code=404, detail=f"Vimages {id} not found")