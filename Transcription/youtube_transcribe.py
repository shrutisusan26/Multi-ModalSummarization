from  youtube_transcript_api import YouTubeTranscriptApi
import json

def get_yt_transcript(url):
    """
    A function to download a transcript from a youtube video link.

    Args:
        url (str): Link to video.

    Returns:
        sentences (dict): Containg transcript and metadata received from Youtube Transcript API.
    """
    try:
        _id = url.split("=")[1].split("&")[0]
    
    except:
        print("Invalid link")

    transcripts = YouTubeTranscriptApi.get_transcripts([_id])
    sentences={}
    for sent in transcripts[0][_id]:
        sentences[sent['start']]=sent['text']
   
    return sentences
            
if __name__=="__main__":
    example_url = "https://www.youtube.com/watch?v=h0e2HAPTGF4"
    with open(r"E:\Multi-Modal Summarization\Data\trans\ml.json", "w") as f:
        json.dump(get_yt_transcript(example_url),f)