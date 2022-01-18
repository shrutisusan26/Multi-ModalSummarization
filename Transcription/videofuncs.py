import cv2
import os
import fleep
from pydub import AudioSegment
from Transcription.bTranscription import uploadtoaz

def getmd(ip):
    cap = cv2.VideoCapture(ip)
    fps = cap.get(cv2.CAP_PROP_FPS)
    dur = cap.get(cv2.CAP_PROP_FRAME_COUNT)/fps
    return dur, fps

def upload(ip,db):
    dir = os.path.join(os.getcwd(),'Data')
    dir = os.path.join(dir,'audio')
    if 'videos' in ip:
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
            end = 0 - len(info.extension)
            fname = ip.split("\\")[-1][:end]
            nfname = os.path.join(dir,fname)
            audio = AudioSegment.from_file(ip, info.extension)
            audio.export(nfname, format="mp3")
            blob_name = fname
    return (uploadtoaz(ip,db,blob_name,dir))

def getdir(file):
    mtype = file.content_type
    mtype = mtype.split('/')
    if mtype[0] == 'audio':
        dir = os.path.join(os.getcwd(),'Data')
        dir = os.path.join(dir,'audio')
        return dir
    elif mtype[0] == 'video':
        dir = os.path.join(os.getcwd(),'Data')
        dir = os.path.join(dir,'videos')
        return dir
    #Can do for transcript upload too
    else:
        return 'Invalid'