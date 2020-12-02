# -*- coding: utf-8 -*-
"""
Created on Mon Nov 30 18:57:56 2020

@author: Ganyu Wang

Use the saved model to predict 

"""
import numpy as np
import os
import PIL
import PIL.Image

import tensorflow as tf
from tensorflow import keras

from tensorflow.keras.layers import Dense, Dropout, Flatten
from tensorflow.keras.layers import Conv2D, MaxPooling2D, Conv2DTranspose
from tensorflow.keras import layers
from tensorflow.keras.preprocessing.image import ImageDataGenerator

from Model import Transform_model
from Utility import load_image
from Loss import extractor

import matplotlib.pyplot as plt

assert tf.test.is_gpu_available()
assert tf.test.is_built_with_cuda()


#%% setting
model_path = "model/transform_model_epoch_40.h5"

test_image_path = "test_content_image/20123.jpg"
style_image_path = "style_img/impression_sunrise.jpg"
transfer_image_save_path = "test_content_image/predict_20123.jpg"

test_video_path = "test_content_video/video1.mp4"


#%% build model
inputs = keras.Input(shape=(256, 256, 3))
outputs = Transform_model(inputs)
transform_model = keras.Model(inputs=inputs, outputs=outputs)

# load weights
transform_model.load_weights(model_path)


#%% image style transfer

test_img = load_image(test_image_path)
pred_img = transform_model.predict(test_img)
style_image = load_image(style_image_path)

plt.figure()
plt.imshow(style_image[0,])


plt.figure()
plt.imshow(test_img[0,])

plt.figure()
plt.imshow(pred_img[0,])

# save predict figure
plt.savefig("predict.png")


#%% video style transfer

import cv2
import numpy as np

# Create a VideoCapture object and read from input file
# If the input is the camera, pass 0 instead of the video file name
cap = cv2.VideoCapture(test_video_path)

video = []

# Check if camera opened successfully
if (cap.isOpened()== False): 
  print("Error opening video stream or file")

# Read until video is completed
while(cap.isOpened()):
  # Capture frame-by-frame
  ret, frame = cap.read()
  if ret == True:
    resized_frame = cv2.resize(frame, (256, 256))
    video.append(resized_frame)
    
  else: 
    break

# When everything done, release the video capture object
# Closes all the frames
cap.release()
cv2.destroyAllWindows()

video = np.array(video) / 255

# transfer video
transfer_video = transform_model.predict(video)
transfer_video *= 255
transfer_video = transfer_video.astype(np.uint8)

# output video

# Define the codec and create VideoWriter object
fourcc = cv2.VideoWriter_fourcc(*'mp4v')
out = cv2.VideoWriter('output.mp4',fourcc, 30, (256,256)) # fps, (size)

for i in range(transfer_video.shape[0]):    
    frame = transfer_video[i]

    # write the flipped frame
    out.write(frame)

# Release everything if job is finished
cap.release()
out.release()
cv2.destroyAllWindows()

