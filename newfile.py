from os import path
from pydub import AudioSegment
import os
# assign files

dir = os.path.join(os.getcwd(),'Data')
dir = os.path.join(dir,'audio')
input_file = os.path.join(dir,"input.mp3")
output_file = "result.wav"
  
# convert mp3 file to wav file
sound = AudioSegment.from_mp3(input_file)
sound.export(output_file, format="wav")