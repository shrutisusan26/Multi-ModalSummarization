from  youtube_transcript_api import YouTubeTranscriptApi


def get_yt_transcript(url):
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
    example_url = "https://www.youtube.com/watch?v=qLvwlsCjMfY&ab_channel=TheMysticaLand"
    get_yt_transcript(example_url)