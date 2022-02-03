from  youtube_transcript_api import YouTubeTranscriptApi

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
    example_url = "https://www.youtube.com/watch?v=wbtpOhIP9Bc&t=67s&ab_channel=CrashCourse"
    get_yt_transcript(example_url)