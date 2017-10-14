import os
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.neighbors import KNeighborsClassifier
from sklearn.ensemble import RandomForestClassifier
import plainUtil as utils
from sklearn import tree
import pandas as pd
import numpy as np
import os
from sklearn.externals.six import StringIO
import pydotplus
from sklearn.metrics import accuracy_score ,f1_score, precision_score, recall_score, classification_report, confusion_matrix

#from sklearn.tree import DecisionTreeClassifier
#model = DecisionTreeClassifier(max_depth=4, min_samples_split=4, min_samples_leaf=4)
class ProcessMiner(object):

	def __init__(self,modeFileName , answer_txt  , questionNumber , algoType):
		if questionNumber == "1":			
			train = pd.read_csv(os.path.join(os.path.dirname(__file__), 'datasets', 'train_rel_2_2.tsv'), header=0, delimiter="\t", quoting=3)
		if questionNumber == "2":
			train = pd.read_csv(os.path.join(os.path.dirname(__file__), 'datasets', 'assaignments1.csv'))
		if questionNumber == "3":
			train = pd.read_csv(os.path.join(os.path.dirname(__file__), 'datasets', 'assaignments2.csv'))
		if questionNumber == "4":
			train = pd.read_csv(os.path.join(os.path.dirname(__file__), 'datasets', 'assaignments3.csv'))
		self.ANSWER_RESPONSE = answer_txt
		self.MODEL_FILE = modeFileName
		self.MODEL_ACCURACY = 0.0
		self.x = train.EssayText
		self.y = train.Score1
		self.getwhat = algoType + "-" + questionNumber + ":"
		self.ANSWER_RESPONSE=[self.ANSWER_RESPONSE]

		self.ANSWER_RESPONSE = np.asarray(self.ANSWER_RESPONSE)
		self.x_train , self.x_test , self.y_train , self.y_test = train_test_split(self.x ,self.y ,test_size = .2 , random_state = 42)
		self.vectorizer = CountVectorizer(analyzer = "word",tokenizer = None, preprocessor = None, stop_words = None, max_features = 5000)
		if algoType == 'rc':			
			self.classifierEstimator = RandomForestClassifier(n_estimators = 100)
		if algoType == 'dc':
			self.classifierEstimator = tree.DecisionTreeClassifier()
		if algoType =='kc':
			self.classifierEstimator = KNeighborsClassifier()

	# def getwhat(self ):
	# 	return algoType + "-" + questionNumber + ":"

	# gets the document term matrix
	def process(self,vectorizer, model , x_test_  ):
		testVect = self.testingProcess(vectorizer , x_test_ )		
		result = model.predict(testVect)
		return result

	def testingProcess(self,vect , x_test__):
		test = vect.transform(x_test__)
		return test

	def createModel(self,x_train__ , y_train__):	
		self.vectorizer.fit(x_train__)
		train_data_features = self.vectorizer.transform(x_train__)
		train_data_features = self.vectorizer.fit_transform(x_train__)
		self.classifierEstimator.fit( train_data_features, y_train__ )
		
		return  self.vectorizer

	def saveModelClassifier(self, data_features ,y_train__ ):	
		
		utils.saveClassifier( self.classifierEstimator , self.MODEL_FILE)

	def scoreClassify( self, model ,vectorizer ):
		""" returns a score in list """
		return self.process(vectorizer, model, self.x_test )

	def naive_accuracy(self,true, pred):
	    number_correct = 0
	    i = 0
	    for i, y in enumerate(true):
	        if pred[i] == y:
	            number_correct += 1.0
	    return number_correct / len(true)

	def scoreAccuracy(self,model , vectorizer, last_pred):
		"""gets the  accuracy  value"""	
		last_pred = self.process(vectorizer, model, self.ANSWER_RESPONSE   )
		y_score =  np.asarray(last_pred)
		return accuracy_score(y_score ,last_pred )

	def scoreAccuracyHack(self,model , vectorizer, last_pred):
		"""gets the  accuracy  value"""	
		last_pred = self.process(vectorizer, model, self.ANSWER_RESPONSE   )
		y_score =  np.asarray(last_pred)
		return self.naive_accuracy(y_score ,last_pred )