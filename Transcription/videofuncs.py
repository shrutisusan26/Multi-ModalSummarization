import cv2
import os
import fleep
from pydub import AudioSegment
from Transcription.bTranscription import uploadtoaz
import moviepy.editor as mp
from helper import dirgetcheck

def getmd(ip):
    """
    A function to get return certain video details

    Args:
        ip (str): File path to video file

    Returns:
        dur,fps (int,int): Returns video duration and original framerate
    """
    print(ip)
    cap = cv2.VideoCapture(ip)
    fps = cap.get(cv2.CAP_PROP_FPS)
    dur = cap.get(cv2.CAP_PROP_FRAME_COUNT)/fps
    return dur, fps

def upload(ip,db,upload=True):
    """
    A function to check file and convert to an mp3 if required and trigger an upload 
    to azure and a Speech to Text API.

    Args:
        ip (str): File path.
        db (MongoClient): Client to perform CRUD operations on database.
        upload (bool, optional): A flag to set if file needs to be uploaded or just converted.
        Defaults to True.

    Returns:
        dict: Containing timestamps and sentences.
    """
    dir = dirgetcheck('Data','audio')
    if not upload or 'videos' in ip:
        video_clip =ip
        clip = mp.VideoFileClip(video_clip)
        blob_name = video_clip.split("\\")[-1][:-3]+'mp3'
        if not os.path.isfile(os.path.join(dir,blob_name)):
            clip.audio.write_audiofile(os.path.join(dir,blob_name))
            sound = AudioSegment.from_mp3(os.path.join(dir,blob_name))
            sound = sound.set_channels(1)
            sound.export(os.path.join(dir,blob_name), format="mp3")
    elif 'audio' in ip:
        if '.mp3' in ip.split("\\")[-1]:
            blob_name=ip.split("\\")[-1]
        else:
            with open(ip, "rb") as file:
                info = fleep.get(file.read(128))
            end = 0 - len(info.extension[0])
            fname = ip.split("\\")[-1][:end]+"mp3"
            nfname = os.path.join(dir,fname)
            audio = AudioSegment.from_file(ip, info.extension[0])
            audio.export(nfname, format="mp3")
            blob_name = fname
    print(blob_name)
    return (uploadtoaz(db,blob_name,dir))

def getdir(file):
    """
    A function to check uploaded file's metadata and determine the correct directory of 
    storing.

    Args:
        file (StreamObject): A Stream Object containg the uploaded file.

    Returns:
        dir (str): Directory path or Invalid.
    """
    mtype = file.content_type
    mtype = mtype.split('/')
    if mtype[0] == 'audio':
        dir = dirgetcheck('Data','audio')
        return dir
    elif mtype[0] == 'video':
        dir = dirgetcheck('Data','videos')
        return dir
    else:
        return 'Invalid'