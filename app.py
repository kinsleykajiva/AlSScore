from flask import Flask , \
request , render_template , redirect , url_for, session, flash, g, make_response, send_file , jsonify
from flask_cache import Cache
from flask_login import login_required , current_user
from flask.ext.login import LoginManager, login_user, logout_user, current_user, login_required
from functools import wraps
import DBMsql as conx
import re
import os
from flask.ext.bcrypt import Bcrypt



app=Flask(__name__)

app.secret_key = 'kinsleykajiva'+str(os.urandom(11))
app.config['TEMPLATES_AUTO_RELOAD'] = True
bcrypt = Bcrypt(app)
db=conx.ConnectClass(bcrypt)



#algorithm for Short Response scoring aka AlSScore

@app.route("/")
def index():
	# This the index page
	if "username" in session and "userType" == session:
		if session['userType'] == "Student":
			redirect(url_for("/student/"))
		else:
			redirect(url_for("/teacher/"))


	return render_template("login.html")


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
	db.SaveAnswerResponse('put the arguments in this )

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

@app.before_request
def before_request():
    # When you import jinja2 macros, they get cached which is annoying for local
    # development, so wipe the cache every request.
    if 'localhost' in request.host_url or '0.0.0.0' in request.host_url:
        app.jinja_env.cache = {}


if __name__ == '__main__':
	app.jinja_env.auto_reload = True
	app.config['TEMPLATES_AUTO_RELOAD'] = True
	app.run(debug=True, host='127.0.0.1')
	# r=db.registerTeacherUser("1kajivakinsley@gmail.com", "qwerty")
	# print(r)
	# s=db.loginTeacherUser("1kajivakinsley@gmail.com", "qwerty")
	# print("xxxx :: "+s)
	
	

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

	
	
	







