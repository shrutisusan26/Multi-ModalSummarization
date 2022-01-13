import torch as th
#from torch.utils.data import Dataset
import pandas as pd
import os
import numpy as np
import ffmpeg
import re

class VideoLoader():
    def __init__(
            self,
            fname,
            framerate=1,
            size=112,
            centercrop=False,
    ):
        """
        Args:
        """
        self.fname = fname
        self.centercrop = centercrop
        self.size = size
        self.framerate = framerate

    def _get_video_dim(self, video_path):
        print("Inside get_video_dim")
        print(os.path.isfile(video_path))
        probe = ffmpeg.probe(video_path)
        #print(probe)
        video_stream = next((stream for stream in probe['streams']
                             if stream['codec_type'] == 'video'), None)
        width = int(video_stream['width'])
        height = int(video_stream['height'])
        print("Exiting get_video_dim")
        return height, width

    def _get_output_dim(self, h, w):
        print("Inside get_o/p_dim")
        if isinstance(self.size, tuple) and len(self.size) == 2:
            return self.size
        elif h >= w:
            return int(h * self.size / w), self.size
        else:
            return self.size, int(w * self.size / h)

    def vidfeat(self):
        print(self.fname)
        video_path = self.fname
        opn =video_path[0:10]
        opn = opn.replace(r'\.','')
        opn = opn.replace('\\','')
        opn = opn.replace(':','')
        opf = os.path.join(os.getcwd(),'Data')
        output_file = opn+'op.npy'
        output_file = os.path.join(opf,output_file)
        print(video_path,output_file)
        print(os.path.isfile(video_path))
        if not(os.path.isfile(output_file)) and os.path.isfile(video_path):
            print('Decoding video: {}'.format(video_path))
            try:
                print("Using FFMPEG to Probe")
                h, w = self._get_video_dim(video_path)
            except Exception as e:
                print(e)
                print('ffprobe failed at: {}'.format(video_path))
                return {'video': th.zeros(1), 'input': video_path,
                        'output': output_file}
            print("Done probing...")
            height, width = self._get_output_dim(h, w)
            print(self.framerate)
            cmd = (
                ffmpeg
                .input(video_path)
                .filter('fps', fps=self.framerate)
                .filter('scale', width, height)
            )
            if self.centercrop:
                x = int((width - self.size) / 2.0)
                y = int((height - self.size) / 2.0)
                cmd = cmd.crop(x, y, self.size, self.size)
            out, _ = (
                cmd.output('pipe:', format='rawvideo', pix_fmt='rgb24')
                .run(capture_stdout=True, quiet=True)
            )
            if self.centercrop and isinstance(self.size, int):
                height, width = self.size, self.size
            video = np.frombuffer(out, np.uint8).reshape([-1, height, width, 3])
            video = th.from_numpy(video.astype('float32'))
            video = video.permute(0, 3, 1, 2)
            print("here")
        else:
            video = th.zeros(1)
            print("okay.... this is sad")
        return {'video': video, 'input': video_path, 'output': output_file}
