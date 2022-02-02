import time
from helper import dirgetcheck
import swagger_client as cris_client
from config import config 
from azure.storage.blob  import BlobServiceClient, BlobBlock
from azure.storage.blob import generate_blob_sas, BlobSasPermissions
import os
from datetime import datetime, timedelta
import uuid
from azure.core.exceptions import ResourceNotFoundError
from entities.dbschemas import transEntity
from Transcription.process_transcript import readj
from helper import dirgetcheck

SUBSCRIPTION_KEY = config.api_key
SERVICE_REGION = "centralindia"
DESCRIPTION = "Lecture Video"
LOCALE = "en-US"
container_name = 'forlecture'
account_name = config.storage_name
account_key = config.storage_key

def _paginate(api, paginated_object):
    """
    This function returns a generator over all items of the array that 
    the paginated object `paginated_object` is part of.

    Raises:
        Exception: If data could not be found.

    Yields:
        Array: Contains the paginated objects data.
    """
    yield from paginated_object.values
    typename = type(paginated_object).__name__
    auth_settings = ["apiKeyHeader", "apiKeyQuery"]
    while paginated_object.next_link:
        link = paginated_object.next_link[len(
            api.api_client.configuration.host):]
        paginated_object, status, headers = api.api_client.call_api(link, "GET",
                                                                    response_type=typename, auth_settings=auth_settings)
        if status == 200:
            yield from paginated_object.values
        else:
            raise Exception(
                f"could not receive paginated data: status {status}")

def transcribe(url_with_sas,blob_name,db):
    """
    Starts a speech to text API on a blob uploaded to azure.

    Args:
        url_with_sas (str): URL to the uploaded blob with SAS token appended.
        blob_name (str): Name of blob.
        db (MongoClient): Client that allows CRUB operations on database.
    
    Returns:
        results (dict): Containing timestamps and transcript sentences.
    """
    configuration = cris_client.Configuration()
    configuration.api_key["Ocp-Apim-Subscription-Key"] = SUBSCRIPTION_KEY
    configuration.host = f"https://{SERVICE_REGION}.api.cognitive.microsoft.com/speechtotext/v3.0"

    client = cris_client.ApiClient(configuration)
    api = cris_client.DefaultApi(api_client=client)
    if(transcription_id := db.trans.find_one({"blob_name": blob_name}) is None):
        properties = {
            "wordLevelTimestampsEnabled": True,
            "diarizationEnabled": True,
            "destinationContainerUrl": config.container_sas_uri,
        }
        
        transcription_definition = cris_client.Transcription(
        display_name=blob_name[:-3],
        description=DESCRIPTION,
        locale=LOCALE,
        content_urls=[url_with_sas],
        properties=properties
        )   

        created_transcription, status, headers = api.create_transcription_with_http_info(
            transcription=transcription_definition)

        transcription_id = headers["location"].split("/")[-1]
        completed = False

        while not completed:
            time.sleep(5)
            transcription = api.get_transcription(transcription_id)
            if transcription.status in ("Failed", "Succeeded"):
                completed = True
                item={'transcription_id':transcription_id,'blob_name':blob_name}
                db.trans.insert_one(transEntity(item))
    else:
        transcription_id = db.trans.find_one({"blob_name": blob_name})
        transcription_id = transcription_id['transcription_id']

    transcription = api.get_transcription(transcription_id)
    if transcription.status == "Succeeded":
        pag_files = api.get_transcription_files(transcription_id)
        for file_data in _paginate(api, pag_files):
            if file_data.kind != "Transcription":
                continue
            global container_name
            results_url = file_data.links.content_url.split(container_name)
            blob_service_client = BlobServiceClient.from_connection_string(config.connect_str)
            blob_client = blob_service_client.get_blob_client(container=container_name, blob=results_url[1][1:])
            fname = transcription_id+'result.json'
            dir = dirgetcheck('Data','trans')
            with open(os.path.join(dir,fname),'wb') as dw:
                dw.write(blob_client.download_blob().readall())
            results = readj(os.path.join(dir,fname))
            return results
    elif transcription.status == "Failed":
        results = 'Failed'
        return results

def uploadtoaz(db,blob_name,dir):  
    """
    A function to upload a blob to azure and triggers a speech to text API on it.

    Args:
        db (MongoClient): Allows database CRUD operations.
        blob_name (str): Name of blob.
        dir (str): Path to directory where file is stored.

    Returns:
        results (dict): Containing timestamps and transcript sentences.
    """
    block_list=[]
    chunk_size=8192 
    blob_service_client = BlobServiceClient.from_connection_string(config.connect_str)
    blob_client = blob_service_client.get_blob_client(container=container_name, blob=blob_name)

    try: 
        blob_client.get_blob_properties()
        print("File exists")

    except ResourceNotFoundError:
        print("\nUploading to Azure Storage as blob:\n\t" + blob_name)
        with open(os.path.join(dir,blob_name), "rb") as data:
            while True:
                read_data = data.read(chunk_size)
                if not read_data:
                    break
                blk_id = str(uuid.uuid4())
                blob_client.stage_block(block_id=blk_id,data=read_data) 
                block_list.append(BlobBlock(block_id=blk_id))
        blob_client.commit_block_list(block_list)
   
    sas_blob = generate_blob_sas(account_name=account_name, 
                                container_name=container_name,
                                blob_name=blob_name,
                                account_key=account_key,
                                permission=BlobSasPermissions(read=True),
                                expiry=datetime.utcnow() + timedelta(hours=1))
    url_with_sas = 'https://'+account_name+'.blob.core.windows.net/'+container_name+'/'+blob_name+'?'+sas_blob
    results = transcribe(url_with_sas,blob_name,db)
    return results

        
    


