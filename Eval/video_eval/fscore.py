import cv2
import numpy as np
import os
import scipy.spatial

def cosine_distance_between_two_images(v1, v2, th):
    """
    Calculates cosine similarity between 2 vectors.

    Args:
        v1 (np arr): Vector corresponding to a frame.
        v2 (np arr): Vector corresponding to a frame.

    Returns:
        int: Cosine similarty between the 2 vectors.
    """
    cs = 1- scipy.spatial.distance.cosine(v1, v2)
    if cs >=th:
        return True
    else:
        return False

def imfeat(file):
    lst = []
    directory = os.listdir(file)
    #print(directory)
    #print(directory)
    for picture in directory:
        img = cv2.imread(os.path.join(file,picture))
        img = cv2.resize(img,(320,320),interpolation=cv2.INTER_AREA)
        img = img.flatten().tolist() # because classifiers require it to be flat
        #print(len(img))
        lst.append(img)
    return np.array(lst)

def calc(a,p):
    tp = 0
    fp = 0
    found =[]
    for i,v1 in enumerate(p):
        for j,v2 in enumerate(a):
            if cosine_distance_between_two_images(v1,v2,0.98) and j not in found:
                #print(i,j)
                tp+=1
                found.append(j)
                break
        #print("Hi")
    fp = len(p)-tp
    fn = len(a)-tp
    #print(tp,fp)
    return tp,fp,fn
       
def calcfscore(afile,pfile):
    actual = imfeat(afile)
    pred = imfeat(pfile)
    tp,fp,fn = calc(actual,pred)
    print(tp,fp,fn,len(pred),len(actual))
    precision = tp /(tp+fp)
    recall = tp/(tp+fn)
    f = 2 * precision * recall /(precision + recall)
    return f, float(tp/len(pred))


if __name__=="__main__":
    p1 = r'E:\Multi-Modal Summarization\Eval\video_eval\Generated_Keyframes'
    p2 = r'E:\Multi-Modal Summarization\Eval\video_eval\Actual_Images\Simran annotated'
    total =0
    for i in (os.listdir(p2)):
            score,per = calcfscore(os.path.join(p2,i),os.path.join(p1,i))
            print(score,per)
            print(str(i))
            total+=score
    print(total/len(os.listdir(p2)))
