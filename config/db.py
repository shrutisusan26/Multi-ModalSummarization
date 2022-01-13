from dotenv import load_dotenv
from pymongo import MongoClient
import os

load_dotenv()  # take environment variables from .env.
mongodb_key = os.getenv('mongodb_key')
conn = MongoClient(mongodb_key)