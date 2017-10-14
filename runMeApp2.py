import os
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.ensemble import RandomForestClassifier
from sklearn.naive_bayes import MultinomialNB
from sklearn.feature_extraction.text import CountVectorizer, TfidfTransformer
import plainUtil as utils
from sklearn.pipeline import Pipeline
import pandas as pd
import numpy as np
from sklearn.externals.six import StringIO
import pydotplus
from sklearn.metrics import accuracy_score ,f1_score, precision_score, recall_score, classification_report, confusion_matrix

train = pd.read_csv(os.path.join(os.path.dirname(__file__), 'datasets', 'train_rel_2_2.tsv'), header=0, delimiter="\t", quoting=3)
QUEST = "to replicate the experiment you need to know how much vinegar to put in the containers there needs to be a control and you also need to know the shape of the objects because shape could have an effect on how much material gets dissolved"
#get data into columns
x = train.EssayText
y = train.Score1
bow_transformer = CountVectorizer(analyzer = "word").fit(x)

messages_bow = bow_transformer.transform(x)
tfidf_transformer = TfidfTransformer().fit(messages_bow)
messages_tfidf = tfidf_transformer.transform(messages_bow)

spam_detector = MultinomialNB().fit(messages_tfidf, y)
message4 = "QUEST" #x[3]
bow4 = bow_transformer.transform([message4])
tfidf4 = tfidf_transformer.transform(bow4)

new_sample = spam_detector.predict(tfidf4)[0]
print ('predicted:', new_sample)
print ('expected:', y[3])
all_predictions = spam_detector.predict(messages_tfidf)
print ('accuracy', accuracy_score(y, all_predictions))

#0.550682261209

new_y =new_sample
new_x = message4


bow_transformer_new = CountVectorizer(analyzer = "word").fit(new_x)

messages_bow_new = bow_transformer_new.transform(new_x)
tfidf_transformer = TfidfTransformer().fit(messages_bow_new)
bow4 = bow_transformer_new.transform([new_x])
messages_tfidf_new = tfidf_transformer.transform(messages_bow_new)
all_predictions = spam_detector.predict(messages_tfidf_new)

print ('accuracy', accuracy_score(new_y, all_predictions))
print("precision_score ",precision_score(new_y, all_predictions))















