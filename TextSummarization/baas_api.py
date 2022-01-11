from fastapi import FastAPI, status ,HTTPException
import numpy as np
from transformers import BertTokenizer, BertModel
from fastapi.responses import JSONResponse
from bson.objectid import ObjectId
from clustering import gen_summary, clean
from models.summary import Article
from schemas.summary import summaryEntity
from fastapi.middleware.cors import CORSMiddleware
# OPTIONAL: if you want to have more information on what's happening, activate the logger as follows
import logging
#logging.basicConfig(level=logging.INFO)
import matplotlib.pyplot as plt
from baas import generate_sentence_embeddings
from config.db import conn
db = conn.Vidsum


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
# @app.get("/embedding/")
# async def get_embeddings(sentence:str,response_body=SentenceEmbedding):
#     # Load pre-trained model tokenizer (vocabulary)
#     print(sentence)
#     tokenizer = BertTokenizer.from_pretrained('bert-base-uncased')
#     # Load pre-trained model (weights)
#     model = BertModel.from_pretrained('bert-base-uncased',
#                                     output_hidden_states = True, # Whether the model returns all hidden-states.
#                                     )
#     sentence_embedding = generate_sentence_embeddings(model,tokenizer,sentence)
#     sentence_embedding = {"sentence_embedding":sentence_embedding.tolist()}
#     return sentence_embedding

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

@app.get('/result/{id}',response_description="Retrieves the summary", response_model=str)
async def result(id:str):
   if( article := db.Article.find_one({"_id": ObjectId(id)}) ) is not None:
        return '.'.join([article['article'].split('.')[i] for i in article['order']])
   raise HTTPException(status_code=404, detail=f"Article {id} not found")