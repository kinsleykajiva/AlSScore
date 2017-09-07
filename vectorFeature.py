"""
author Kinsley Kajiva

This  will converting my text feature or raw text as match vector to be used in my vector space 
Also to be used in the Rainforest Algorithm and also in Baruta Algorithm 


"""
import gensim
import gensim.models.word2vec as w2v
from nltk.tokenize import word_tokenize
import nltk as nl
import multiprocessing
import logging
import codecs
import os
import sys

datatest = "datasets/ObjectOrientedProgramminginC4thEdition.txt"

class VectorFeature(object):
	"""docstring for VectorMAker"""
	#this is a deminensions size of the vector matrix	
	number_of_featuers = 300
	# minimum word count threadhold
	min_word_count_threshHold = 5
	#processing ability
	thread_count = multiprocessing.cpu_count()
	context_size = 7
	#doqnsample setting for frequncey
	downSampling = 1e-3
	def __init__(self,raw_txt):
		self.raw_txt = raw_txt

	def wordVec(self):
		gensim.models.tfidfmodel.df2idf

	def rawtakenizer(self):
		self.localTokenizer = nl.data.load("tokenizers/punkt/english.pickle")
		#split text into sentences
		self.sentences = self.localTokenizer.tokenize(self.raw_txt)

	def convertvector(self):
		
		#self.vec =""
		self.vec = w2v.Word2Vec(sg=1,seed=1,workers=multiprocessing.cpu_count(),size=300,min_count=5,window=7,sample=(1e-3))
		#build status or model properties to get vobulary size
		self.vec.build_vocab(self.sentences)
		#train Model
		self.vec.train(self.sentences, total_examples=self.vec.corpus_count, epochs=self.vec.iter)
		#save the trained model
		
		self.vec.save(os.path.join("cores/caches", "model003.w2v"))
		print("done creating a model")
		#print("vocabulary size in lenght:: ",len(self.vec.vocab))

	def loadModel(self, modelName):
		
		self.vec = w2v.Word2Vec.load(os.path.join("cores/caches",modelName + ".w2v"))

	def processVector(self, query_txt):		
		return self.vec.most_similar(query_txt)


if __name__ == '__main__':
	program = os.path.basename(sys.argv[0])
	logger = logging.getLogger(program)
	logging.basicConfig(format='%(asctime)s: %(levelname)s: %(message)s')
	logging.root.setLevel(level=logging.INFO)
	logger.info("running %s" % ' '.join(sys.argv))

	raw_txt = u""
	# loading all the file into memory in the raw_txt
	# with codecs.open(datatest, 'r', "utf-8") as file:
	# 	raw_txt += file.read()

	make = VectorFeature(raw_txt)
	make.rawtakenizer()
	#make.convertvector()
	make.loadModel("model001")
	print( make.vec )
	make.loadModel("model002")
	print( make.vec )		
	#make.processVector("object")
	


		
		




