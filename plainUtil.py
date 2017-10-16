from sklearn.feature_extraction.text import CountVectorizer
from sklearn.ensemble import RandomForestClassifier
from sklearn import tree
import nltk
from collections import Counter
from nltk.corpus import stopwords
from nltk.corpus import wordnet
from nltk import WordNetLemmatizer
import numpy as np
import re
from time import gmtime, strftime
import datetime, time

question = "Describe two ways the student could have improved the experimental design and/or validity of the results"

Algorithm_IN_USE = "RandomForestClassifier"

def bag_of_words(list_raw_txt):
	classifier = tree.DecisionTreeClassifier()

	classifier.fit(X_train, y_train)

def getNowDateTime():
    "2017-10-05 05:12:57"
    return strftime("%Y-%m-%d %H:%M:%S", gmtime())
def getNowDate():
    "2017-10-05"
    return strftime("%Y-%m-%d", gmtime())

def getNowTime():
    "2017-10-05 05:12:57"
    return strftime("%H:%M:%S:%MS", time.localtime())

def processMeaning(abr):
    return 'Random Forest' if abr == 'rc' else 'Decision Tree' if abr == 'dc' else 'KNeighbors'


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
    import os    
    joblib.dump(model, os.path.join("cores/caches/models",model_name+'.pkl'))

def openClassierr(model_name):
    """ open saved model """
    from sklearn.externals import joblib
    import os
    #return joblib.load( model_name+'.pkl')
    return joblib.load( os.path.join("cores/caches/models",model_name+'.pkl'))

def isModelFileAvailable(modeleFileName):
    """ check if the model file even exists  """
    import os
    return os.path.isfile(os.path.join("cores/caches/models",modeleFileName + '.pkl'))
    
def get_wordnet_pos(treebank_tag):
    """
    Description
    -----------
    Takes in a POS tag from TreeBank
    and maps it to WordNet POS tag.
    
    Parametesr
    ----------
    treebank_tag: str
    
    Returns
    -------
    wordnet_tag: str
    """
    if treebank_tag.startswith('J'):
        wordnet_tag = wordnet.ADJ
    elif treebank_tag.startswith('V'):
        wordnet_tag = wordnet.VERB
    elif treebank_tag.startswith('N'):
        wordnet_tag = wordnet.NOUN
    elif treebank_tag.startswith('R'):
        wordnet_tag = wordnet.ADV
    else:
        wordnet_tag = u'n' # treat unknown as noun
        
    return wordnet_tag

def preprocess(passage, error_handling='strict'): 
    """
    Description
    -----------
    Pre-processes esssay by stripping punctuation,
    POS tagging and lemmatization.
    
    Parameters
    ----------
    passage: string
        a passage to be pre-processed.
        
    error_handling: string
        how to handle encode/decode erros
        can be 'replace', 'ignore', etc.
    
    Returns
    -------
    processed_passage: string
    """
    
    assert error_handling in ['strict',
                              'ignore',
                              'replace']
    
    # initialize
    wnl = WordNetLemmatizer()
    
    # remove punctuation and loweracase
    rmv = passage.replace('@', '')
    passage_nopunc = re.sub(r"[{}]".format(rmv), ' ', 
                            passage.lower())
    
    # tokenize passage
    tokens = nltk.word_tokenize(passage_nopunc)
    
    # POS tag and transform to wordnet POS notation
    # NB: elements in `wn_tagged` are (word, POS) tuples.
    wn_tagged = [(t[0], get_wordnet_pos(t[1])) \
                 for t in nltk.pos_tag(tokens)]
    
    # lemmatize
    lemmatized = [wnl.lemmatize(*t) for t in wn_tagged]
    
    return " ".join(lemmatized)


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



if __name__ == '__main__':    
    s = "some additional information that we would need to replicate the experiment is how much vinegar should be placed in each identical container how or what tool"
    #tim = getNowDateTime().replace(":","_").replace("-","_").replace(" ","_")
    #print(tim)
    print(processMeaning('dc'))









