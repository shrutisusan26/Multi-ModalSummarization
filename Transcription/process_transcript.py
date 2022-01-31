import json
from TextSummarization.sentence_preprocessing import check_sentence_length

def find_sentence_for_frame(start_time,end_time,sentences):
    res = {key: val for key, val in filter(lambda sub: int(float(sub[0])) >= start_time and
                                   int(float(sub[0])) <= end_time, sentences.items())}
    return res

def clean(sentences):
    sentence = {key:val for key, val in sentences.items() if check_sentence_length(val.split())}
    return sentence
    
def readj(name):
    with open(name) as f:
        data = json.load(f)
    phrases = data['recognizedPhrases']
    sentences = {}
    transcript = data['combinedRecognizedPhrases'][0]['display']
    for i in range(len(phrases)-1):
        start_time = phrases[i]['offsetInTicks']//(10**7)
        l_sentences = phrases[i]['nBest'][0]['display'].split(".")[:-1]
        if len(l_sentences)>1:
            end_time = phrases[i+1]['offsetInTicks']//(10**7)
            delta = (end_time-start_time)/len(l_sentences)
            for j in l_sentences:
                sentences[start_time] = j + "."
                start_time = start_time+delta
        else:
            sentences[start_time] = phrases[i]['nBest'][0]['display']
    l_sentences = phrases[-1]['nBest'][0]['display'].split(".")[:-1]
    start_time = phrases[-1]['offsetInTicks']//(10**7)
    if len(l_sentences)>1:
        delta = (phrases[-1]['durationInTicks']//(10**7))/len(l_sentences)
        for j in l_sentences:
            sentences[start_time] = j + "."
            start_time = start_time+delta
    else:
        sentences[start_time] = phrases[i]['nBest'][0]['display']
    print(sentences)
    sentences = clean(sentences)
    return sentences

def process_yttranscript(transcript):
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

if __name__=="__main__":
    readj("transcript.json")
    
    
