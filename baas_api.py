from fastapi import FastAPI, status ,HTTPException, File, UploadFile
import shutil
import os
import numpy as np
from fastapi.responses import JSONResponse
from bson.objectid import ObjectId
from TextSummarization.tclustering import gen_summary, clean
from VideoSummarization.vclustering import vsum
from models.summary import Article,Vidpath
from schemas.summary import summaryEntity,vsummaryEntity
from Transcription.bTranscription import upload
from fastapi.middleware.cors import CORSMiddleware
# OPTIONAL: if you want to have more information on what's happening, activate the logger as follows
import logging
#logging.basicConfig(level=logging.INFO)
import matplotlib.pyplot as plt
from TextSummarization.baas import generate_sentence_embeddings
from config.db import conn, start

db = conn.Vidsum
start()

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
    dir = os.path.join(os.getcwd(),'Data')
    dir = os.path.join(dir,'videos')
    if not os.path.isdir(dir):
        os.makedirs(dir)
    destination = os.path.join(dir,file.filename)
    try:
        with open(destination,"wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
    finally:
        transcription = upload(destination)
        file.file.close()
    return {"transcript": transcription, "dpath":destination}

@app.post("/vsummary", response_description="Post path for video summary")
async def vsummary(path: Vidpath):
    path = path.dict()
    print(path)
    ordering,fr = vsum(path['path'])
    print(ordering,fr)
    item={'path':path,'order':ordering,'fr':fr}
    response =  db.Vimage.insert_one(vsummaryEntity(item))
    item['id']= str(response.inserted_id)
    return JSONResponse(status_code=status.HTTP_201_CREATED, content=item['id'])

@app.post("/summary", response_description="Post article for summary")
async def summary(article:Article):
    article = article.dict()
    print(article)
    article = clean(article['article'])
    ordering = gen_summary(article)
    item={'article':article,'order':ordering}
    response =  db.Article.insert_one(summaryEntity(item))
    item['id']= str(response.inserted_id)
    summary=[]
    article=article.split(".")
    for index in ordering:
            summary.append(article[index])
    item['summ']="".join(summary)
    print(item['order'])
    return JSONResponse(status_code=status.HTTP_201_CREATED, content=item['id'])

@app.get('/tresult/{id}',response_description="Retrieves the summary", response_model=str)
async def tresult(id:str):
   if( article := db.Article.find_one({"_id": ObjectId(id)}) ) is not None:
        return '.'.join([article['article'].split('.')[i] for i in article['order']])
   raise HTTPException(status_code=404, detail=f"Article {id} not found")

@app.get('/vresult/{id}',response_description="Retrieves the video images", response_model=str)
async def vresult(id:str):
   if( path := db.Vimages.find_one({"_id": ObjectId(id)}) ) is not None:
        return ''.join(i for i in path['order'])
   raise HTTPException(status_code=404, detail=f"Vimages {id} not found")