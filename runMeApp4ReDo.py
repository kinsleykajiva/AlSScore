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
		if questionNumber is "1":			
			train = pd.read_csv(os.path.join(os.path.dirname(__file__), 'datasets', 'train_rel_2_2.tsv'), header=0, delimiter="\t", quoting=3)
		if questionNumber is "2":
			train = pd.read_csv(os.path.join(os.path.dirname(__file__), 'datasets', 'assaignments1.csv'))
		if questionNumber is "3":
			train = pd.read_csv(os.path.join(os.path.dirname(__file__), 'datasets', 'assaignments2.csv'))
		if questionNumber is "4":
			train = pd.read_csv(os.path.join(os.path.dirname(__file__), 'datasets', 'assaignments3.csv'))
		self.ANSWER_RESPONSE = answer_txt
		self.MODEL_FILE = modeFileName
		self.MODEL_ACCURACY = 0.0
		self.x = train.EssayText
		self.y = train.Score1
		self.ANSWER_RESPONSE=[self.ANSWER_RESPONSE]
		self.ANSWER_RESPONSE = np.asarray(self.ANSWER_RESPONSE)
		self.x_train , self.x_test , self.y_train , self.y_test = train_test_split(self.x ,self.y ,test_size = .2 , random_state = 42)
		self.vectorizer = CountVectorizer(analyzer = "word",tokenizer = None, preprocessor = None, stop_words = None, max_features = 5000)
		if algoType is 'rc':			
			self.classifierEstimator = RandomForestClassifier(n_estimators = 100)
		if algoType is 'dc':
			self.classifierEstimator = tree.DecisionTreeClassifier()
		if algoType is 'kc':
			self.classifierEstimator = KNeighborsClassifier()

	# gets the document term matrix
	def process(self,vectorizer, model , x_test_  ):
		testVect = self.testingProcess(vectorizer , x_test_ )		
		result = model.predict(testVect)
		return result

	def testingProcess(self,vect , x_test__):
		test = vect.transform(x_test__)
		return test

	def trainProcess(self,x_train__ , y_train__):	
		self.vectorizer.fit(x_train__)
		train_data_features = self.vectorizer.transform(x_train__)
		train_data_features = self.vectorizer.fit_transform(x_train__)
		
		return train_data_features , self.vectorizer

	def saveModelClassifier(self, data_features ,y_train__ ):	
		self.classifierEstimator.fit( data_features, y_train__ )
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


access = ProcessMiner(
	"model0010-KNeighborsClassifier1" + utils.getNowDateTime().replace(":","_").replace("-","_").replace(" ","_") , 
	" A constructor is called whenever an object is created, whereas a function needs to be called explicitely. Constructors do not have return type, but functions have to indicate a return type ", 
	"3" , 'rc')
# lets check if the model file exists 
IS_MODEL_AVAILABLE = utils.isModelFileAvailable(access.MODEL_FILE)

if IS_MODEL_AVAILABLE is False:	
	#training start
	print("training model.")
	train_data_features , vectorizer = access.trainProcess(access.x_train , access.y_train)
	access.saveModelClassifier( train_data_features, access.y_train )

print("using model file")
vectorizer = access.vectorizer.fit(access.x_train)
if IS_MODEL_AVAILABLE:

	vectorizer.transform(access.x_train)
	vectorizer.fit_transform(access.x_train)

model = utils.openClassierr(access.MODEL_FILE)
	
testing_predicts = access.scoreClassify(model ,vectorizer )
access.MODEL_ACCURACY = accuracy_score(access.y_test , testing_predicts)
print("MODEL_ACCURACY :: ", access.MODEL_ACCURACY )

pred = access.process(vectorizer, model, access.ANSWER_RESPONSE   )
print(type(pred))
print(np.array_str(pred))
print("Score:: ",pred[0])

# 1 :: 0.480582524272
# after creating file and training got val 0.572815533981
# method 2=> reading from a file directly got val 0.587378640777
# method 2 => traing and read got val 0.611650485437
# mothod 2 => read got val 0.611650485437
# KNeighborsClassifier = > traing and read got val 461165048544
# KNeighborsClassifier = > read got val 461165048544
# 




