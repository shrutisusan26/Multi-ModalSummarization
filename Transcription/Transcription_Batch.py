from azure.storage.blob.baseblobservice import BaseBlobService
from azure.storage.blob import BlobServiceClient
import numpy as np
from azure.storage.blob.models import BlobPermissions
from datetime import datetime, timedelta
import requests
import os
import moviepy.editor as mp
import config

account_name = config.storage_name
account_key = config.storage_key
container_name = 'forlecture' # for example, `test`
blob_name = 'record.mp3' # for example, `whatstheweatherlike.wav`
subscription_key, service_region = config.api_key, "centralindia"

clip = mp.VideoFileClip("Search in an almost sorted array  GeeksforGeeks.mp4")
# Insert Local Audio File Path

if not os.path.isfile("record.mp3"):
    clip.audio.write_audiofile("record.mp3")
    
    blob_service_client = BlobServiceClient.from_connection_string(config.connect_str)
    blob_client = blob_service_client.get_blob_client(container=container_name, blob=blob_name)
    print("\nUploading to Azure Storage as blob:\n\t" + blob_name)
    with open(blob_name, "rb") as data:
        blob_client.upload_blob(data)
    


def get_token(subscription_key, service_region):
    fetch_token_url = "https://centralindia.api.cognitive.microsoft.com/speechtotext/v3.0/"
    headers = {
        'Ocp-Apim-Subscription-Key': subscription_key
    }
    response = requests.post(fetch_token_url, headers=headers)
    access_token = str(response.text)
    return access_token

blob_service = BaseBlobService(
    account_name=account_name,
    account_key=account_key
)

sas_token = blob_service.generate_blob_shared_access_signature(container_name, blob_name, permission=BlobPermissions.READ, expiry=datetime.utcnow() + timedelta(hours=1))
url_with_sas = blob_service.make_blob_url(container_name, blob_name, sas_token=sas_token)
access_token = get_token(subscription_key, service_region)

endpoint = "https://centralindia.api.cognitive.microsoft.com/speechtotext/v3.0/transcriptions"

audio_blob_url_with_sas = url_with_sas # it's from STEP 1.
r = requests.get(audio_blob_url_with_sas)
data = {
  "contentUrls": url_with_sas,
  "properties": {
    "wordLevelTimestampsEnabled": "true"
  },
  "locale": "en-US",
  "displayName": "Transcription of file using default model for en-US"
}

res = requests.post(endpoint, data=data)
print(res.text)