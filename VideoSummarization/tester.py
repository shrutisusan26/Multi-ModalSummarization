import scipy.spatial
import numpy as np
def cosine_distance_between_two_images(v1, v2):
    return (1- scipy.spatial.distance.cosine(v1, v2))


op = np.load('E:\Multi-Modal Summarization\VideoSummarization\Data\EMulti-Mop.npy')
print(cosine_distance_between_two_images(op[6],op[9]))