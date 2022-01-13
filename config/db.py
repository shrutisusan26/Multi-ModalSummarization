from dotenv import load_dotenv
from pymongo import MongoClient
import os

load_dotenv()  # take environment variables from .env.
mongodb_key = os.getenv('mongodb_key')
conn = MongoClient(mongodb_key)

def start()
    dir = os.path.join(os.path.dirname(os.getcwd()),'Data')
    if not os.path.isdir(dir):
        os.makedirs(dir)