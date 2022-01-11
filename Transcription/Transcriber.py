import speech_recognition as sr
import moviepy.editor as mp
import azure.cognitiveservices.speech as speechsdk
import os
import time
import pprint
import json
import srt
import datetime
import config
# Insert Local Video File Path 

clip = mp.VideoFileClip("Lecture 30-20211028 0641-1.mp4")
# Insert Local Audio File Path
clip.audio.write_audiofile("record.wav")

path = os.getcwd()
# Creates an instance of a speech config with specified subscription key and service region.
# Replace with your own subscription key and region identifier from here: https://aka.ms/speech/sdkregion
speech_key, service_region = config.api_key, "eastus"
speech_config = speechsdk.SpeechConfig(subscription=speech_key, region=service_region)

audio_filename = "record.wav"
audio_input = speechsdk.audio.AudioConfig(filename=audio_filename)

# Creates a recognizer with the given settings
speech_config.speech_recognition_language="en-US"
speech_config.request_word_level_timestamps()

speech_config.enable_dictation()
speech_config.output_format = speechsdk.OutputFormat(1)

speech_recognizer = speechsdk.SpeechRecognizer(speech_config=speech_config, audio_config=audio_input)

#result = speech_recognizer.recognize_once()
all_results = []
results = []
transcript = []
words = []

#https://docs.microsoft.com/en-us/python/api/azure-cognitiveservices-speech/azure.cognitiveservices.speech.recognitionresult?view=azure-python
def handle_final_result(evt):
    import json
    all_results.append(evt.result.text) 
    results = json.loads(evt.result.json)
    transcript.append(results['DisplayText'])
    confidence_list_temp = [item.get('Confidence') for item in results['NBest']]
    max_confidence_index = confidence_list_temp.index(max(confidence_list_temp))
    words.extend(results['NBest'][max_confidence_index]['Words'])



done = False

def stop_cb(evt):
    print('CLOSING on {}'.format(evt))
    speech_recognizer.stop_continuous_recognition()
    global done
    done= True
    
speech_recognizer.recognized.connect(handle_final_result) 
#Connect callbacks to the events fired by the speech recognizer    
#speech_recognizer.recognizing.connect(lambda evt: print('RECOGNIZING: {}'.format(evt)))
#speech_recognizer.recognized.connect(lambda evt: print('RECOGNIZED: {}'.format(evt)))
speech_recognizer.session_started.connect(lambda evt: print('SESSION STARTED: {}'.format(evt)))
speech_recognizer.session_stopped.connect(lambda evt: print('SESSION STOPPED {}'.format(evt)))
speech_recognizer.canceled.connect(lambda evt: print('CANCELED {}'.format(evt)))
# stop continuous recognition on either session stopped or canceled events
speech_recognizer.session_stopped.connect(stop_cb)
speech_recognizer.canceled.connect(stop_cb)

speech_recognizer.start_continuous_recognition()

while not done:
    time.sleep(.5)
    
print("Printing all results:")
print(all_results)

with open("transcription.txt","w") as f:
    f.write(" ".join(all_results))