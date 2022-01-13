import json

def find_sentence_for_frame(start_time,end_time,sentences):
    res = {key: val for key, val in filter(lambda sub: int(sub[0]) >= start_time and
                                   int(sub[0]) <= end_time, sentences.items())}
    print(res)

with open('transcript.json') as f:
   data = json.load(f)

phrases = data['recognizedPhrases']
sentences = {}
transcript = data['combinedRecognizedPhrases'][0]['display']

for i in phrases:
    start_time = i['offsetInTicks']//(10**7)
    sentences[start_time] = i['nBest'][0]['display'] 
find_sentence_for_frame(30,70,sentences)
    
