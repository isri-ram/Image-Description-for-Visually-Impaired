from nltk.translate.bleu_score import corpus_bleu
from tensorflow.keras.models import load_model
import pickle
from tqdm.notebook import tqdm

# Load the model from the Pickle file
with open('tokenizer.pkl', 'rb') as file:
    tokenizer = pickle.load(file)
with open('features.pkl', 'rb') as file:
    features = pickle.load(file)

model = load_model('best_model.h5')
max_length = 35
# validate with test data
actual, predicted = list(), list()

for key in tqdm(test):
    # get actual caption
    captions = mapping[key]
    # predict the caption for image
    y_pred = predict_caption(model, features[key], tokenizer, max_length)
    # split into words
    actual_captions = [caption.split() for caption in captions]
    y_pred = y_pred.split()
    # append to the list
    actual.append(actual_captions)
    predicted.append(y_pred)

# calcuate BLEU score
print("BLEU-1: %f" % corpus_bleu(actual, predicted, weights=(1.0, 0, 0, 0)))
print("BLEU-2: %f" % corpus_bleu(actual, predicted, weights=(0.5, 0.5, 0, 0)))