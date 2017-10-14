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
#get data into columns
x = train.EssayText
y = train.Score1


# delete me start
vectorizer = CountVectorizer(analyzer = "word",tokenizer = None, preprocessor = None, stop_words = None, max_features = 5000)
vectorizer.fit(x,y)
test_data_features = vectorizer.transform(x)
train_data_features = vectorizer.fit_transform(x)

clf = RandomForestClassifier(n_estimators = 100)
clf.fit(train_data_features , y)
predict_result = clf.predict(
	vectorizer.transform([QUEST])
	)

print(predict_result)

# v= len(["" for index ,label in  enumerate(y ) if label == predict_result[index] ])

# print("xxxxxxx %f" %(float(v)/len(y)))

print(accuracy_score( y , predict_result))

#end of start

exit()

print(x.shape)
print(y.shape)
#print(y.value_counts())
print("::::::::::")



x_train , x_test , y_train , y_test = train_test_split(x ,y ,test_size = .25 , random_state = 42)
# print(x_train)
# print(x_test)

#print(y_train)
# print(y_train)
# print(y_train.shape)
# print(type(y_train))
# exit()

clean_ = []

vectorizer = CountVectorizer(analyzer = "word",tokenizer = None, preprocessor = None, stop_words = None, max_features = 5000)

#vectorizer.fit(x_train)

# gets the document term matrix
train_data_features = vectorizer.fit_transform(x_train)


test_data_features = vectorizer.transform(x_test)
QUEST_featue = vectorizer.transform([QUEST])


np.asarray(train_data_features)

print("Training the random forest ..")


forest = RandomForestClassifier(n_estimators = 100)

forest = forest.fit( train_data_features, y_train )


np.asarray(test_data_features)

#result = forest.predict(test_data_features)
result = forest.predict(QUEST_featue)


print("Score:: ",result)



print(accuracy_score(y, result))
#print(recall_score(train_data_features, result))
# print(precision_score(y_test, result))
# print(classification_report(y_test, result))


































