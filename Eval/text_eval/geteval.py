import numpy as np
from pythonrouge.pythonrouge import Pythonrouge
from typing import List
from rouge_metric import PyRouge
from rouge import Rouge

def test_text(list_of_pred, list_of_reference):
    #rouge = PyRouge(rouge_n=(1, 2, 4), rouge_l=True, rouge_w=True, rouge_w_weight=1.2, rouge_s=True, rouge_su=True, skip_gap=4)
    #score = rouge.evaluate(list_of_pred, list_of_reference)
	rouge = Rouge()
	score = rouge.get_scores(list_of_pred,list_of_reference,avg=True)
	print(score)
	return score
	
#user_sum - a numpy array of shape(user, frame_selected)
def get_f1_score(pred_sum,user_sum,f1_type='max'):
	max_val=max(len(pred_sum),user_sum.shape[1])
	sum=np.zeros(max_val,dtype=int)
	gen_sum=np.zeros(max_val,dtype=int)
	sum[:len(pred_sum)]=pred_sum
	
	f_scores=[]
	for user in range(user_sum.shape[0]):
		gen_sum[:user_sum.shape[1]]=user_sum[user]
		overlap= sum & gen_sum #can also define differently
		precision= sum(overlap)/sum(sum)
		recall= sum(overlap)/sum(gen_sum)
		if(precision+recall==0):
			f_scores.append(0)
		else:
			f_scores.append(2*precision*recall*100/(precision+recall))
	if(f1_type=='max'):
		return max(f_scores)
	else:
		return sum(f_scores)/len(f_scores) #avg
#summary- list of strings
#ref can be a string/list

if __name__=="__main__":
		a =['this is her','ok','he began by starting a five person war cabinet and included chamberlain as lord president of the council']
		p = ['this her','what','he began his premiership by forming a five-man war cabinet which included chamberlain as lord president of the council']
		for i,j in zip(a,p):
			test_text(i,j)
