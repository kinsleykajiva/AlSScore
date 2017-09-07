from sklearn.feature_extraction.text import CountVectorizer
from sklearn.ensemble import RandomForestClassifier
from sklearn import tree
import nltk
from nltk.corpus import stopwords
import numpy as np
import re

question = "Describe two ways the student could have improved the experimental design and/or validity of the results"

def bag_of_words(list_raw_txt):
	classifier = tree.DecisionTreeClassifier()

	classifier.fit(X_train, y_train)


def review_to_wordlist( review, remove_stopwords=False ):
    #review_text = re.sub("[^a-zA-Z]"," ", review)
        #
        # 3. Convert words to lower case and split them
    words = review.lower().split()
        #
        # 4. Optionally remove stop words (false by default)
    if remove_stopwords:
       stops = set(stopwords.words("english"))
       words = [w for w in words if not w in stops]
        #
        # 5. Return a list of words
    return words

def saveClassifier(model , model_name):
    from sklearn.externals import joblib
    joblib.dump(model, model_name+'.pkl')

def openClassierr(model_name):
    """ open saved model """
    from sklearn.externals import joblib
    return joblib.load( model_name+'.pkl')
    




def bag_of_words(raw_txt):
	
	# Initialize the "CountVectorizer" object, which is scikit-learn's
    # bag of words tool.
    # analyzer :{‘word’, ‘char’, ‘char_wb’} , Whether the feature should be made of word or character n-grams
    vectorizer = CountVectorizer(analyzer = "word")
    # fit_transform() does two functions: First, it fits the model
    # and learns the vocabulary; second, it transforms our training data
    # into feature vectors. The input to fit_transform should be a list of
    # strings.
    train_data_features = vectorizer.fit_transform([raw_txt])

    return train_data_features
def makep():
    print("::::::::::::::::::::::::::::::::::::::::")
    print("::::::::::::::::::::::::::::::::::::::::")
    print("::::::::::::::|||||||||||||||||||::::::::")
    print("::::::::::::::::::::::::::::::::::::::::")
    print("::::::::::::::::::::::::::::::::::::::::")

s = "some additional information that we would need to replicate the experiment is how much vinegar should be placed in each identical container how or what tool"
print(bag_of_words(s))









