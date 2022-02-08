import os
import json
import pandas as pd
import re
import numpy as np

data = {'article':[],'summary':[]}
os.mkdir(r"E:\Multi-Modal Summarization\Eval\Dataset\Wikihow\ActualWH")
os.mkdir(r"E:\Multi-Modal Summarization\Eval\Dataset\Wikihow\SummaryWH")
dir = r'E:\Data\wikihow_extractive_compressed_5000\Data'
counter = 0
for jfile in os.listdir(dir):
    with open(os.path.join(dir,jfile),'r') as f:
        json_obj = json.load(f)

    for i in json_obj:
        text = []
        summary = []
        for sents in i['src']:
            text.append(' '.join(sents))
        labels = np.array(i['labels'])
        idx = np.where(labels == 1)
        for j in idx[0]:
            summary.append(text[j])
        text = re.sub("( ')+","'",'\n'.join(text))
        summary = re.sub("( ')+","'",'\n'.join(summary))
        text = re.sub('( \.)+',". ",text)
        summary = re.sub('( \.)+',". ",summary)
        text = re.sub('( ,)+',",",text)
        summary = re.sub('( ,)+',",",summary)
        with open(f'E:/Multi-Modal Summarization/Eval/Dataset/Wikihow/ActualWH/{counter}.txt',"w",encoding='utf8') as f:
            f.write(text)
        with open(f'E:/Multi-Modal Summarization/Eval/Dataset/Wikihow/SummaryWH/{counter}.txt',"w",encoding='utf8') as f:
            f.write(summary)
        counter +=1
