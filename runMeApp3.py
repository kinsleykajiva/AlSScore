import os
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.ensemble import RandomForestClassifier
import plainUtil as utils
import pandas as pd
import numpy as np
from sklearn.externals.six import StringIO
import pydotplus
from sklearn.metrics import accuracy_score ,f1_score, precision_score, recall_score, classification_report, confusion_matrix

train = pd.read_csv(os.path.join(os.path.dirname(__file__), 'datasets', 'train_rel_2_2.tsv'), header=0, delimiter="\t", quoting=3)
QUEST = "to replicate the experiment you need to know how much vinegar to put in the containers there needs to be a control and you also need to know the shape of the objects because shape could have an effect on how much material gets dissolved"
QUEST = "you would need many more pieces of information to replicate the experiment . you would need the type of samples to begin with in the procedure . you would also need to know the amount of vinegar used in each container . you would also need to know exactly how to mass the samples and what types of container to use plastic for example might alter the results"
#get data into columns
x = train.EssayText
y = train.Score1

print(x.shape)
print(y.shape)
#print(y.value_counts())
print("::::::::::")

QUEST=[QUEST]
QUEST = np.asarray(QUEST)
#print(QUEST.shape)



x_train , x_test , y_train , y_test = train_test_split(x ,y ,test_size = .2 , random_state = 42)


vectorizer = CountVectorizer(analyzer = "word",tokenizer = None, preprocessor = None, stop_words = None, max_features = 5000)
forest = RandomForestClassifier(n_estimators = 100)
#vectorizer.fit(x_train)

# gets the document term matrix

def process(vectorizer, model , x_test_  ):

	testVect = testingProcess(vectorizer , x_test_ )
	#QUEST_featue = vectorizer.transform([QUEST])	
	
	result = model.predict(testVect)
	#Quest_result = forest.predict(QUEST_featue)

	return result

def testingProcess(vect , x_test__):
	test = vect.transform(x_test__)
	return test
#training start
vectorizer.fit(x_train)
train_data_features = vectorizer.transform(x_train)
train_data_features = vectorizer.fit_transform(x_train)
#np.asarray(train_data_features)
#model = forest.fit( train_data_features, y_train )
#end of training

#save model to file
#utils.saveClassifier( forest , "model0005")
model = utils.openClassierr("model0005")

pred = process(vectorizer, model, x_test   )
print("Score:: ",pred)
print(accuracy_score(y_test, pred))
#recreate
pred = process(vectorizer, model, QUEST   )
print("Score:: ",pred)
y_score =  np.asarray(pred)
print(accuracy_score(y_score, pred))

print("precision_score ",precision_score(y_score, pred))

def naive_accuracy(true, pred):
    number_correct = 0
    i = 0
    for i, y in enumerate(true):
        if pred[i] == y:
            number_correct += 1.0
    return number_correct / len(true)

print( naive_accuracy(y_score , pred) )











