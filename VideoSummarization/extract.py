import torch as th
import numpy as np
from VideoSummarization.video_loader import VideoLoader
from torch.utils.data import DataLoader
from VideoSummarization.model.model import get_model
from VideoSummarization.preprocessing import Preprocessing
import torch.nn.functional as F
import gc

def get_feat(video_path,fr):
    dataset = VideoLoader(
        video_path,
        framerate=fr,
        size=112,
        centercrop=True,
    )
    preprocess = Preprocessing()
    model = get_model()

    with th.no_grad():
            data = dataset.vidfeat()
            print("hi")
            input_file = data['input']
            output_file = data['output']
            if len(data['video'].shape) > 3:
                print('Computing features of video')
                print(data['video'].shape)
                video = data['video']
                print(video.shape)
                if len(video.shape) == 4:
                    video = preprocess(video)
                    print(video.shape)
                    print("HERE")
                    n_chunk = len(video)
                    features = th.cuda.FloatTensor(n_chunk, 2048).fill_(0)
                    for i in range(n_chunk):
                        min_ind = i 
                        max_ind = (i + 1)
                        video_batch = video[min_ind:max_ind].cuda()
                        batch_features = model(video_batch)
                        batch_features = F.normalize(batch_features, dim=1)
                        features[min_ind:max_ind] = batch_features
                    features = features.cpu().numpy()
                    features = features.astype('float16')
                    np.save(output_file, features)
                    print(output_file)
                    gc.collect()
                    th.cuda.empty_cache()
            else:
                print('Video {} already processed.'.format(input_file))
