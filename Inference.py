#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pickle
import numpy as np
from tensorflow.keras.applications.vgg16 import VGG16, preprocess_input
from tensorflow.keras.preprocessing.image import load_img, img_to_array
from tensorflow.keras.preprocessing.sequence import pad_sequences
from tensorflow.keras.models import Model,load_model


# In[2]:

global model
model = load_model('best_model.h5')

# In[3]:

global vgg_model
vgg_model = VGG16()
# restructure the model
vgg_model = Model(inputs=vgg_model.inputs, outputs=vgg_model.layers[-2].output)


# In[4]:

global tokenizer
tokenizer = pickle.load(open('tokenizer.pkl', 'rb'))

# In[5]:


def preprocess_encode(image_path,vgg_model):
    # load image
    image = load_img(image_path, target_size=(224, 224))
    # convert image pixels to numpy array
    image = img_to_array(image)
    # reshape data for model
    image = image.reshape((1, image.shape[0], image.shape[1], image.shape[2]))
    # preprocess image for vgg
    image = preprocess_input(image)
    # extract features
    feature = vgg_model.predict(image, verbose=0)
    return feature


# In[6]:


def idx_to_word(integer, tokenizer):
    for word, index in tokenizer.word_index.items():
        if index == integer:
            return word
    return None


# In[7]:


# generate caption for an image
def predict_caption(model, image, tokenizer):
    max_length = 35
    # add start tag for generation process
    in_text = 'startseq'
    # iterate over the max length of sequence
    for i in range(max_length):
        # encode input sequence
        sequence = tokenizer.texts_to_sequences([in_text])[0]
        # pad the sequence
        sequence = pad_sequences([sequence], max_length)
        # predict next word
        yhat = model.predict([image, sequence], verbose=0)
        # get index with high probability
        yhat = np.argmax(yhat)
        # convert index to word
        word = idx_to_word(yhat, tokenizer)
        # stop if word not found
        if word is None:
            break
        # append word as input for generating next word
        in_text += " " + word
        # stop if we reach end tag
        if word == 'endseq':
            break
      
    return in_text


# In[8]:


def clean_text(text):
  text = text.replace("startseq", "")
  text = text.replace("endseq", "")
  return text


# In[9]:

def caption_this_image(image_path):
    feature = preprocess_encode(image_path,vgg_model)
    predicted_caption = predict_caption(model, feature, tokenizer)
    caption = clean_text(predicted_caption)
    return caption

