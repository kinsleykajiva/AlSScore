
import pymysql
from pymysql import escape_string as thwart
from passlib.hash import sha256_crypt
# from  constantsSettongs import *
import constantsSettongs as cons
from flask.ext.bcrypt import Bcrypt
import itertools 
import plainUtil as utils



""" """

class ConnectClass(object):
	"""This class will handle all the database saving and reading operations"""
	def __init__(self  , crypt = "" ):
		self.crypt = crypt
		self.db = pymysql.connect( host = cons.LOCALHOST , user = cons.USER , passwd = cons.PASSWORD , db=cons.DATABASE )
		self.cursor=self.db.cursor()
		
		"""
			Check if table exists and create the table if the table does noto exist 
			Also to initialise variables
		"""
		

	
	def createQuestionsTable(self):
		table="CREATE TABLE IF NOT EXISTS " 
		+ cons.QUESTIONS_TABLE + " ( id INT(11) NOT NULL AUTO_INCREMENT, " 
		+ cons.COL_QUESTION_NUMBER + " VARCHAR(3) NOT NULL, " + cons.COL_QUESTION 
		+ " TEXT NOT NULL, " +	cons.COL_QUESTION_MARKS+ " VARCHAR(5) NOT NULL, " 
		+ cons.COL_QUESTION_SOLUTIONS+" TEXT NOT NULL, " + cons.COL_QUESTION_STOPWORDS+" TEXT NOT NULL, " + cons.COL_QUESTION_PICKLE 
		+" VARCHAR(111) NOT NULL,"  + "PRIMARY KEY(id) );"
		try:
			self.cursor.execute(table) 
			self.db.commit()
		except Exception as e:
				raise e


	def registerStudentUser( self, username , password ):
		try:
			password = self.crypt.generate_password_hash(password).decode('utf-8') # encript the password
			query=self.cursor.execute("SELECT * FROM " + cons.STUDENT_USERS_TABLE + " WHERE " + cons.COL_STUDENT_USER + " = '"+username+"'")
			if int(query) > 0 :
				return "taken"
			else:
				self.cursor.execute(" INSERT INTO " + cons.STUDENT_USERS_TABLE + "(" + cons.COL_STUDENT_USER + "," + cons.COL_STUDENT_PASSWORD + ") VALUES ( '"+username+"' , ' "+password+" ' )")
				self.db.commit()
				return "done"
		except Exception as ex:
			return "error" +str(ex)

	def registerTeacherUser( self, username , password ):
		try:
			password = self.crypt.generate_password_hash(password).decode('utf-8') # encript the password
			query=self.cursor.execute("SELECT * FROM " + cons.TEACHER_USERS_TABLE + " WHERE " + cons.COL_TEACHER_USER + " = '" + username+"'")
			if int(query) > 0 :
				return "taken"
			else:
				self.cursor.execute(" INSERT INTO " + cons.TEACHER_USERS_TABLE + " (" + cons.COL_TEACHER_USER + " , " + cons.COL_TEACHER_PASSWORD + ") VALUES ( '" + username + "' , ' " + password +" ' )")
				self.db.commit()
				return "done"
		except Exception as ex:
			return "error"
		

	def loginStudentUser(self, username , password ):
		""" Will return exist if user is found in the database and if not found will return new  """
		try:
			
			query=self.cursor.execute("SELECT * FROM " + cons.STUDENT_USERS_TABLE + " WHERE " + cons.COL_STUDENT_USER + " = '"+username+"' ")			

			if int(query) > 0 :
				query = self.cursor.fetchone()[2].strip()

				if self.crypt.check_password_hash( query ,  password ) :

					return "exist"
				else:
					return "password_error"
			else:			
				return "new"
		except Exception as ex:
			return "error" 

	def loginTeacherUser(self, username , password ):
		""" Will return exist if user is found in the database and if not found will return new  """
		try:			
			query=self.cursor.execute("SELECT * FROM " + cons.TEACHER_USERS_TABLE + " WHERE " + cons.COL_TEACHER_USER + " = '"+username+"' ")

			if int(query) > 0 :

				query = self.cursor.fetchone()[2].strip()
				

				if self.crypt.check_password_hash( query ,  password ) :

					return "exist"
				else:
					return "password_error"
				
			else:			
				return "new"
		except Exception as ex:
			return "error"

	def SaveAnswerResponse(self , question_number , response , student , graded_mark , model_file ):
		""" Will save the answer response data to database table<br>Will return done if successfull else error if failed to save"""	
		try:
			query = self.cursor.execute("INSERT INTO "+cons.ANSWER_TABLE + "(" + cons.COL_ANSWER_BY_USER + " , " + cons.COL_ANSWER_NUMBER + " , " + cons.COL_ANSWER_RESPONSE +"," + cons.COL_ANSWER_MARK_AWARDED + " , " +  cons.COL_ANSWER_MODEL_STATE+ " ) VALUES ('" +
			student + "', '" + question_number + "','" + response + "','" + graded_mark + "','" + model_file +  "')")
			self.db.commit()
			return "done"
		except Exception as e:
			return "error" +str(e)
	def saveAnswerRespondedModeled(self  , question , student_name  , response ,question_total ,  score_mark ,model_accuracy , model_file , algorithm_used ):
		""" Will save the answer response data to database table<br>Will return done if successfull else error if failed to save"""	
		turn = ""
		try:
			date__ = utils.getNowDate()	
			st = "INSERT INTO " + cons.ANSWER_TABLE + " ( " + cons.COL_ANSWER_BY_USER + " , " + cons.COL_ANSWER_QUESTION + " , " + cons.COL_ANSWER_RESPONSE + " , " + cons.COL_ANSWER_QUESTION_TOTAL + " , " + cons.COL_ANSWER_MARK_AWARDED + " , " +	cons.COL_ANSWER_MODEL_ACCURACY + "  , " + cons.COL_ANSWER_MODEL_NAME + " , " + cons.COL_ANSWER_DATE + " , "+cons.COL_ANSWER_ALGO+") VALUES ( '" + student_name + "' , '" + question + "' , '"+response+"' , '"+question_total+"' , '"+score_mark+"' , '"+model_accuracy+"' , '"+model_file+"' ,'"+date__+"' , '" + algorithm_used + "' ) " 	
			query = self.cursor.execute( st  )
			self.db.commit()
			turn = "done"
		except Exception as e:
			turn = "error"+str(e)

		return str(turn)
		
	def getStudentResults(self , student ):

		try:
			sql = self.cursor.execute( "SELECT * FROM " + cons.ANSWER_TABLE + " WHERE " + cons.COL_ANSWER_BY_USER + " = '" + student + "'" )
			sql_ = self.cursor.fetchall()			
			row = ""
			col_names = list(itertools.chain.from_iterable(sql_))
			# for i , val in enumerate  (sql_):
			# 	print(sql_[i])

			for i , val in enumerate  (sql_):
				row += " <tr>"
				row += "<td> " + sql_[i][2] + " </td>"
				row += "<td> " + sql_[i][3] + " </td>"
				row += "<td> " + sql_[i][5] + " </td>"
				row += "<td> " + sql_[i][8] + " </td>"
				row += "<td> " + sql_[i][9] + " </td>"
				row += "<td> " + sql_[i][6] + " </td>"
				row += "<td> " + sql_[i][7] + " </td>"
				row += " </tr>"
			return (row)
		except Exception as e:
			return "error" + str(e)

	def saveQuestion(self):
		pass

	def updateQuestion(self):
		pass


	def getAllStudentUsers(self):
		
		try:
			sql=self.cursor.execute("SELECT * FROM " + cons.STUDENT_USERS_TABLE)
			sql_=self.cursor.fetchall()
			
			return sql_
		except Exception as e:
			return str(e)

	def __closeDBConnection(self):
		pass

		
if __name__ == '__main__':
	xcon = ConnectClass()
	print(xcon.getStudentResults("kinsley@memail.com"))
	#print(xcon.saveAnswerRespondedModeled("qeust 1 " , "kinsley" , "qwdrqwewewqwq"  , "3" , "2" ,".3423" ,"model001" , "randomForest"))








