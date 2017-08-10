
""" 
This will have all the constants that will be used as references at run time
"""




LOCALHOST = "localhost"
USER = "root"
PASSWORD = "";

DATABASE = "alsscore"

QUESTIONS_TABLE = "question"
COL_QUESTION_NUMBER = "number"
COL_QUESTION = "question"
COL_QUESTION_MARKS = "marks"
COL_QUESTION_SOLUTIONS = "solutions"
COL_QUESTION_STOPWORDS = "stopwords"
COL_QUESTION_PICKLE = "pickle_file"

ANSWER_TABLE = "response"
COL_ANSWER_NUMBER = "question_number"
COL_ANSWER_RESPONSE = "answer"
COL_ANSWER_MARK_AWARDED = "mark_graded"
COL_ANSWER_MODEL_STATE = "model_state" 
COL_ANSWER_BY_USER = "user_student"


STUDENT_USERS_TABLE = "students"
COL_STUDENT_USER = "user"
COL_STUDENT_PASSWORD = "password"

TEACHER_USERS_TABLE = "teacher"
COL_TEACHER_USER = "user"
COL_TEACHER_PASSWORD = "password"


MODEL_FOLDER = "caches/models/" #the pickles model created  by the teacher 
MODEL_MARKED_FOLDER = "caches/model_marked/" # the pickles model used to mark the response this will used for future referencing to check state or acceptability standards






