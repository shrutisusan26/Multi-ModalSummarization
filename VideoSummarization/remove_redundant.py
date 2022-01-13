import skimage.measure
import matplotlib.pyplot as plt
import numpy as np
import cv2
import os
import imghdr
import scipy

def cosine_distance_between_two_images(v1, v2):
    return (1- scipy.spatial.distance.cosine(v1, v2))

def create_imgs_matrix(directory, px_size=50):
    global image_files   
    image_files = []
    # create list of all files in directory     
    folder_files = [filename for filename in os.listdir(directory)]  
    
    # create images matrix   
    counter = 0
    for filename in folder_files: 
        # check if the file is accesible and if the file format is an image
        if not os.path.isdir(directory + filename) and imghdr.what(directory + filename):
            # decode the image and create the matrix
            img = cv2.imdecode(np.fromfile(directory + filename, dtype=np.uint8), cv2.IMREAD_UNCHANGED)
            if type(img) == np.ndarray:
                img = img[...,0:3]
                # resize the image based on the given compression value
                img = cv2.resize(img, dsize=(px_size, px_size), interpolation=cv2.INTER_CUBIC)
                if counter == 0:
                    imgs_matrix = img
                    image_files.append(filename)
                    counter += 1
                else:
                    imgs_matrix = np.concatenate((imgs_matrix, img))
                    image_files.append(filename)
    return imgs_matrix