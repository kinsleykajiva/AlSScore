#!/usr/bin/env python


import os
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.ensemble import RandomForestClassifier
import plainUtil as utils
import pandas as pd
import numpy as np
from sklearn.metrics import accuracy_score ,f1_score, precision_score, recall_score, classification_report, confusion_matrix

if __name__ == '__main__':
    train = pd.read_csv(os.path.join(os.path.dirname(__file__), 'datasets', 'train_rel_2_2.tsv'), header=0, delimiter="\t", quoting=3)
    test = pd.read_csv(os.path.join(os.path.dirname(__file__), 'datasets', 'test_rel_2_2.tsv'), header=0, delimiter="\t",  quoting=3 )
    train_22= pd.read_csv(os.path.join(os.path.dirname(__file__), 'datasets', 'assaignments1.csv') , header=5  )
    #print(train_22)
    
    
    # Initialize an empty list 
    clean_train_reviews = []

    # Loop over each review; create an index i that goes from 0 to the length    

    print("Cleaning and parsing \n")
    for i in range( 0, len(train["EssayText"])):
        clean_train_reviews.append(" ".join(utils.review_to_wordlist(train["EssayText"][i], True)))


    # ****** Create a bag of words from the training set
    #
    print("Creating the bag of words...\n")



    # Initialize the "CountVectorizer" object, which is scikit-learn's
    # bag of words tool.
    vectorizer = CountVectorizer(analyzer = "word",   \
                             tokenizer = None,    \
                             preprocessor = None, \
                             stop_words = None,   \
                             max_features = 5000)

    # fit_transform() does two functions: First, it fits the model
    # and learns the vocabulary; second, it transforms our training data
    # into feature vectors. The input to fit_transform should be a list of
    # strings
    train_data_features = vectorizer.fit_transform(clean_train_reviews)
    print("\n")
    #print(vectorizer.get_feature_names())
    


    # Numpy arrays are easy to work with, so convert the result to an
    # array
    np.asarray(train_data_features)

    # ******* Train a random forest using the bag of words
    #
    print("Training the random forest ..")



    # Initialize a Random Forest classifier with 100 trees
    forest = RandomForestClassifier(n_estimators = 100)

    # Fit the forest to the training set, using the bag of words as
    # features and the Score1 labels as the response variable
    #
    # This may take a few minutes to run
    forest = forest.fit( train_data_features, train["Score1"] )

    # Create an empty list 
    test_ = []

    print("the test set \n")

    for i in range(0,len(test["EssayText"])):
        test_.append(" ".join(utils.review_to_wordlist(test["EssayText"][i], True)))

    # Get a bag of words for the test set, and convert to a numpy array
    # sample test data after the train also can even call froma a  file of type tsv
    QUEST = ["to replicate the experiment you need to know how much vinegar to put in the containers there needs to be a control and you also need to know the shape of the objects because shape could have an effect on how much material gets dissolved"]
    wrongAnswer = ["Return a callable that handles preprocessing and tokenization"]
    test_data_features = vectorizer.transform(QUEST)
    np.asarray(test_data_features)

    # Use the random forest to make label predictions
    print("Predicting test score...\n")
    print("Predicting test score...\n")
    utils.saveClassifier( forest , "model0005")
    model_pickle = utils.openClassierr("model0005")
    result = model_pickle.predict(test_data_features)
    print("Save score to database or file ... \n")
    print("Save score to database or file ... \n")
    utils.makep()
    print("Score:: ",result)
    #exit()
    from sklearn.cross_validation import train_test_split
    x_train , x_test , y_train , y_test = train_test_split(train , train ,random_state = 1)
    print("accuracy ::: ", accuracy_score( train, result))
    exit()
    print("f1 score ::: ", f1_score( y_test, result))
    print("precision_score ::: ", precision_score( y_test, result))
    