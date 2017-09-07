import re
import numpy as np

from sklearn.datasets import load_iris
from sklearn import tree
from sklearn.externals.six import StringIO
import pydot


iris_data = load_iris()

#print(iris_data.data[0]) # prints 1st row
test_idx = [0, 50, 100]

#training data
training_target = np.delete(iris_data.target, test_idx)
traing_data = np.delete(iris_data.data, test_idx, axis=0)

#testing data
test_target = iris_data.target[test_idx]
test_data  = iris_data.data[test_idx]

clf = tree.DecisionTreeClassifier()
clf.fit(traing_data, training_target)

#print (test_target)
#print (clf.predict(test_data))
# if the  two prints are the same then correct classifier

grapgh = pydot.graph_from_dot_data(dot_data.getvalue())
grapgh.write_pdf("testing.pdf")
print(test_data[0] ,test_target[0])


