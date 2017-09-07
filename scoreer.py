
import os
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.ensemble import RandomForestClassifier
import plainUtil as KaggleWord2VecUtility
import pandas as pd
import numpy as np
from sklearn.metrics import accuracy_score



class scoringMecsh(object):
	"""docstring for scoringMecsh"""
	def __init__(self):
		pass
		self.vectorizer = CountVectorizer(analyzer = "word",   \
                             tokenizer = None,    \
                             preprocessor = None, \
                             stop_words = None,   \
                             max_features = 5000)
		

	def initsavedModel(self, answer_testing):
		test_data_features = self.vectorizer.transform([answer_testing])
    	np.asarray(test_data_features)
		
		











