import spacy
import pytextrank
#from process_transcript import readj

def textrank(text):
    nlp = spacy.load('en_core_web_md')


# add PyTextRank to the spaCy pipeline
    nlp.add_pipe("textrank")
    doc = nlp(''.join(text))

   # doc = nlp(text)
    sentindex = []
    i=1
    for sents in doc.sents:
        #print(i)
        #print(sents)
        sentindex.append(sents.start)
        i=i+1
    #print(sentindex)
   # print(len(sentindex))
    #print(doc.sents)
    # examine the top-ranked phrases in the document
    #for p in doc._.phrases:
    #    print('{:.4f} {:5d}  {}'.format(p.rank, p.count, p.text))
    #    print(p.chunks)

    rlist = []    
    for sent in doc._.textrank.summary(limit_sentences=1):
        rlist.append(sentindex.index(sent.start))
    return (rlist)



#sentences=readj('../input/transcription/trans/0f3b4e9e-bb4e-4d57-be6a-628add513284result.json').values()
#textrank(''.join(sentences))