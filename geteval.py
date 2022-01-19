import numpy as np
from rouge_score import rouge_scorer
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
def test_text(summary,reference):
		summ='.'.join(summary)
		reference='.'.join(reference)
		scores=rouge_scorer.RougeScorer(['rouge1', 'rougeL'], use_stemmer=True)
		score = scores.score(summ,reference)
		print(score)
		return score

if __name__=="__main__":
		test_text(['this is her','what'],['this her','ok'])