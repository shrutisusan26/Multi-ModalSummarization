from cgi import test
import json
from fastapi.testclient import TestClient
from geteval import  test_text
from baas_api import app
import re
from sumy.summarizers.lsa import LsaSummarizer as Summarizer
from sumy.parsers.plaintext import PlaintextParser
from sumy.nlp.tokenizers import Tokenizer
from sumy.nlp.stemmers import Stemmer
from sumy.utils import get_stop_words

client = TestClient(app)

localhost="http://127.0.0.1:8000/"

with open(r'\Eval\Dataset\newsroom-release\release\test-stats.jsonl', 'r') as json_file:
    json_list = list(json_file)

pred_sents,ref_sents=[],[]
for json_str in json_list:
    result = json.loads(json_str)  
    if result['density_bin']=='extractive':
        #print(result['text'])
        sents=  re.split(r'[?.]',result['text'])[:-1]
        dictionary={}
        for i,sent in enumerate(sents):
                #print(sent)
                dictionary[str(i)]=re.sub('"','',sent.strip())
        #print(dictionary)         
        summary_id=client.post(localhost+"summary",json={"article":dictionary ,"t_clusters":1,'fpath':"result\\result","order": {}})
        print(summary_id,summary_id.status_code,summary_id.text)
        assert summary_id.status_code == 201
        summary_id=summary_id.json()
        
        text_sum_order= client.get(localhost+f"tresult/{str(summary_id)}")
        assert text_sum_order.status_code == 200
        text_sum_order=text_sum_order.json()
        
        pred_sents.append('.'.join(text_sum_order.values()))
        ref_sents.append(result['summary'])
        break

# def getres(actual,pred,n=30):
#     pred_sents,ref_sents=[],[]
#     with open(pred,'r',encoding="utf8") as f:
#         pred_sents.append(f.read())
#     parser = PlaintextParser.from_file(actual, Tokenizer('english'))
#     stemmer = Stemmer('english')

#     summarizer = Summarizer(stemmer)
#     summarizer.stop_words = get_stop_words('english')
#     text=''
#     for sentence in summarizer(parser.document, n):
#         #print(sentence)
#         text+='. ' +str(sentence)
#     ref_sents.append(text)
#     print(pred_sents[0])
#     print(ref_sents)
#     test_text(pred_sents,ref_sents)

# if __name__ == "__main__":
#     getres(r'E:\Multi-Modal Summarization\Eval\text_eval\Actual_Text\Intro.txt',r'E:\Multi-Modal Summarization\Eval\text_eval\Generated_Text\Intro.txt')
