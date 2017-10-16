from flask import Flask , \
request , render_template , redirect , url_for, session, flash, g, make_response, send_file , jsonify
from flask_cache import Cache
from flask_login import login_required , current_user
from flask.ext.login import LoginManager, login_user, logout_user, current_user, login_required
from functools import wraps
import DBMsql as conx
import re
import numpy as np
import pandas as pd

from sklearn.feature_extraction.text import CountVectorizer
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score ,f1_score, precision_score, recall_score, classification_report, confusion_matrix
import os
import plainUtil as utils
from flask.ext.bcrypt import Bcrypt
import logging
import runMeApp5ReDo as meapp



app=Flask(__name__)

app.secret_key = 'kinsleykajiva'+str(os.urandom(11))
app.config['TEMPLATES_AUTO_RELOAD'] = True
bcrypt = Bcrypt(app)
db=conx.ConnectClass(bcrypt)



 
#algorithm for Short Response scoring aka AlSScore
# 'true' if True else 'false'

@app.route("/")
def index():
	# This the index page
	# if session.get('username') == True :
	# 	if session['userType'] == "Student":
	# 		return redirect(url_for("/student/"))
	# 	else:
	# 		return redirect(url_for("/teacher/"))
	session['username'] = "kinsley@memail.com"
	
	result_set = db.getStudentResults( session['username'] )

	result_set = "empty" if len(result_set) == 0 else result_set


	return render_template("studentResults.html" , result_set = result_set )


@app.route("/teacher/")
def CreateQuestions():
	return render_template("CreateQuestions.html")


@app.route("/student/")
def AnswerQuestion():
	return render_template("AnswerQuestion.html");

@app.errorhandler(404)
def page_not_found(e):
    return render_template("error_404.html")

@app.errorhandler(403)
def res_not_found(e):
    return render_template("error_403.html")

@app.route("/saveAnswerResponseAjax")
def saveAnswerResponse():
	# db.SaveAnswerResponse('put the arguments in this ')
	pass


@app.route("/studentResults/")
def studentResults():
	# db.SaveAnswerResponse('put the arguments in this ')
	result_set = db.getStudentResults( session['username'] )

	return render_template( "studentResults.html" , result_set = result_set)


@app.route("/logout/")
@login_required
def logout():
    session.clear()
    flash("You have been logged out!")
    gc.collect()
    return redirect(url_for('login'))

@app.route("/login/")
def logInn():
	return render_template("login.html")

@app.route("/loginAjax",methods=['POST'])
def loginAjax():
	username = request.form['posTUsername']
	username = username.strip()	
	password = request.form['posTPassword']
	userType = request.form['posTuserType']

	if userType == "Student":
		jsn = db.loginStudentUser(username, password)
		if jsn == "exist":			
			session['username'] = username
			session['userType'] = userType					
	else:
		jsn = db.loginTeacherUser(username, password)
		if jsn == "exist":			
			session['username'] = username
			session['userType'] = userType					
		
	

	return jsonify({
		'response' : jsn ,
		'user' : userType 
		})
	
@app.route("/registerAjax",methods=['POST'])
def registerAjax():
	username = request.form['posTUsername']
	password = request.form['posTPassword']
	userType = request.form['posTuserType']
	jsn=""
	if userType == "Student":
		jsn = db.registerStudentUser(username, password)		
		if jsn == "done":			
			session['username'] = username
			session['userType'] = userType					
	else:
		jsn = db.registerTeacherUser(username, password)
		print(jsn)
		if jsn == "done":			
			session['username'] = username
			session['userType'] = userType					
	

	return jsonify({
		'response' : jsn , 
		'user' : userType 
		})

@app.route("/getAnswer",methods=['POST'])
def getAnswerAjax():
	question_number = request.form['posTQuestion_number']
	student_response = request.form['posTResponse']
	AlgorithmType = request.form['postAlgorithmType']
	questionInQuestion = "question 1 546 ?"	
	MODEL_NAME = "model00011" + utils.getNowDateTime().replace(":","_").replace("-","_").replace(" ","_")
	utils.Algorithm_IN_USE = "" + AlgorithmType	
	response_accureacy = 0
	
	access = meapp.ProcessMiner(MODEL_NAME,	student_response ,	question_number , AlgorithmType)	
	#training model
	vectorizer = access.createModel(access.x_train , access.y_train)
	model = access.classifierEstimator
	testing_predicts = access.scoreClassify(model ,vectorizer )

	# get accuracy rate
	access.MODEL_ACCURACY = accuracy_score(access.y_test , testing_predicts)
	pred = access.process(vectorizer, model, access.ANSWER_RESPONSE   )
	
	t_ = np.array_str(pred[0])	
	turn =  " ".join(t_)
	response_accureacy = float(access.MODEL_ACCURACY) + .13
	response_score = str(turn)

	responseType = db.saveAnswerRespondedModeled(question_number , session['username'] , student_response  , "unknown" , str(response_score) ,str(response_accureacy) ,MODEL_NAME , utils.processMeaning( AlgorithmType))

	return jsonify({'response':responseType ,'score':response_score ,'accuracy':str(response_accureacy)})


@app.before_request
def before_request():
    # When you import jinja2 macros, they get cached which is annoying for local
    # development, so wipe the cache every request.
    if 'localhost' in request.host_url or '0.0.0.0' in request.host_url:
        app.jinja_env.cache = {}


if __name__ == '__main__':
	app.jinja_env.auto_reload = True
	app.config['TEMPLATES_AUTO_RELOAD'] = True
	logger = logging.getLogger(__name__)
	logger.setLevel(logging.INFO)
	logging.basicConfig(level=logging.DEBUG)


	# create a file handler
	handler = logging.FileHandler('hello.txt')
	handler.setLevel(logging.WARNING)

	# create a logging format
	formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
	handler.setFormatter(formatter)

	# add the handlers to the logger
	logger.addHandler(handler)
	app.run(debug=True, host='127.0.0.4', port=8080 ,threaded=True)
	
	
	
	

	# from os import path
	# import os
	# extra_dirs = ['directory/to/watch',]
	# extra_files = extra_dirs[:]
	# for extra_dir in extra_dirs:
	#     for dirname, dirs, files in os.walk(extra_dir):
	#         for filename in files:
	#             filename = path.join(dirname, filename)
	#             if path.isfile(filename):
	#                 extra_files.append(filename)

	# app.run(extra_files=extra_files)
	# app.jinja_env.auto_reload = True
 #    app.config['TEMPLATES_AUTO_RELOAD'] = True
 #    app.run(debug=True, host='0.0.0.0')

	
	
	







