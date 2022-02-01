from dotenv import load_dotenv
from pymongo import MongoClient
import os
load_dotenv( os.path.join(os.getcwd(),'config\.env'))  # take environment variables from .env.
mongodb_key = os.getenv('mongodb_key')
conn = MongoClient(mongodb_key)

def start():
    """
    Startup function to create the Data directory on the server.
    """
    dir = os.path.join(os.getcwd(),'Data')
    if not os.path.isdir(dir):
        os.makedirs(dir)