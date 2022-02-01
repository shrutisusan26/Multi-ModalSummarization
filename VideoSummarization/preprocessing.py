import torch as th

class Normalize(object):
    """
    Class to instantiate Mean and Standard Dev of the tensor in order 
    to normalise them.

    Args:
        object (np arr): Array with video features.
    """

    def __init__(self, mean, std):
        """
        Initialises the mean and std deviation vectors to the values passed.

        Args:
            mean (int): Mean of the tensors.
            std (int): Std dev of the tensors.
        """
        self.mean = th.FloatTensor(mean).view(1, 3, 1, 1)
        self.std = th.FloatTensor(std).view(1, 3, 1, 1)

    def __call__(self, tensor):
        """
        Performs the normalisation once called.

        Args:
            tensor (no arr): Array of video features.

        Returns:
            tensor (np arr): Normalised array of video features.
        """
        tensor = (tensor - self.mean) / (self.std + 1e-8)
        return tensor

class Preprocessing(object):
    """
    Class to instantiate the Normalise class and take care of zero padding
    to make the video features uniform.

    Args:
        object (np arr): Array of video features.
    """

    def __init__(self):
        """
        Calls the Normalise class and sets the normalised tensors.
        """
        self.norm = Normalize(mean=[110.6, 103.2, 96.3], std=[1.0, 1.0, 1.0])

    def _zero_pad(self, tensor, size):
        """
        Appropriately zero pads the vectors to make them uniform.

        Args:
            tensor (np arr): Array of video features.
            size (int): Number of frames in each chunk.

        Returns:
            (np arr): Zero padded array of video features.
        """
        n = size - len(tensor) % size
        if n == size:
            return tensor
        else:
            z = th.zeros(n, tensor.shape[1], tensor.shape[2], tensor.shape[3])
            return th.cat((tensor, z), 0)

    def __call__(self, tensor):
        """
        Performs normalisation and zero padding to return processed array of features.

        Args:
            tensor (np arr): Array of video features.

        Returns:
            tensor (np arr): Processed Array of video features.
        """
        tensor = self._zero_pad(tensor, 16)
        tensor = self.norm(tensor)
        tensor = tensor.view(-1, 16, 3, 112, 112)
        tensor = tensor.transpose(1, 2)
        return tensor
