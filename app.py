from flask import Flask , request , render_template
from flask_cache import Cache
from flask_login import login_required , current_user


app=Flask(__name__)





@app.route("/")
def index():
	# This the index page
	return render_template("login.html")


@app.route("/teacher/<username>")
@login_required
@check_expired
def CreateQuestions(username):
	return render_template("CreateQuestions.html")
	



if __name__ == '__main__':
	app.run(debug=True)










