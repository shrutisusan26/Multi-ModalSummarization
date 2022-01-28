import json

with open('j5XdY5wkVTA.json') as json_file:
    transcript = json.load(json_file)

def process_transcript(transcript):
    curr_sentence = []
    processed = {}
    flag = 1
    curr_time = list(transcript.keys())[0]
    for time,sent in transcript.items():
        sent = sent.split()
        for i in sent:
            if i[-1]==".":
                curr_sentence.append(i)
                processed[curr_time] = " ".join(curr_sentence)
                flag = 0
                curr_sentence = []
            else:
                if flag==0:
                    curr_sentence.append(i)
                    continue
                curr_sentence.append(i)
                flag = 1
        if flag==0:
            curr_time = time
    return processed

print(process_transcript(transcript))
        
            