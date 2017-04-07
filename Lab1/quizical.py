#!/usr/bin/python
# =============================================================================
#        File : Quizical.py
# Description : Quiz Server for Quiz Devices
#      Author : Drew Gislsason
#        Date : 3/8/2017
# =============================================================================
"""
  Quizical is a simple Quiz server suitable for classrooms.

  Verb   | API                             | Description
  ------ | ------------------------------- | --------------------------------------------------------
  GET    | /api/v1/login                   | Login to the quiz. Receive a token for subsequent calls
  PUT    | /api/v1/profile                 | Change password. Receive a token for subsequent calls
  GET    | /api/v1/student/{name}/question | Get the current question with possible answers
  POST   | /api/v1/student/{name}/question | Post answer to the question. Write once.
  GET    | /api/v1/student/{name}/results  | Results so far
  GET    | /api/v1/teacher/quiz            | get the current quiz
  PUT    | /api/v1/teacher/quiz            | start quiz, move quiz on to next question, etc...
  POST   | /api/v1/teacher/quiz            | create a new quiz (clears all student answers)
  DELETE | /api/v1/teacher/quiz            | delete a quiz (by name)
  GET    | /api/v1/teacher/results         | results of current quiz (option for anonymous students)
  GET    | /api/v1/teacher/students        | get list of students
  POST   | /api/v1/teacher/students        | post a list of students

  TODO: Allow throwing bad values at framework
  TODO: Add multiple instructors
  TODO: Allow students to take quiz at their own pace
  TODO: Allow quizes to expire (e.g. allow a quiz to expire after 24 hours)
  TODO: Database of quizes
  TODO: Provide hooks into grading systems such as Canvas

  Places to host: Heroku, OpenShift
"""
from flask import Flask, request
import random
import string
import base64
import json
import sys

# ============================== Data ====================================

# create the global objects
app = Flask(__name__)

PORT = 4242

# bit map of access rights
ACCESS_STUDENT    = 0
ACCESS_TEACHER    = 1

# TODO: figure out how to make application global and thread safe
quiz = {
  "name": "python",
  "questions": {
    "1" : [ "How do you create a variable with the value 5 in Python?",
      " A. var x = 5",
      " B. def x = 5",
      "*C. x = 5",
      " D. import 5" ],
    "2": [ "How do you create a function in Python?",
      "*A. def my_func(param=None):",
      " B. int my_func(var param):",
      " C. proc my_func(int param):",
      " D. my_func(param=5)" ],
    "3": [ "How do you create a for loop from 1 to 10 in Python?",
      " A: for(i = 1 to 10)",
      " B: for i = 1 to 10 do",
      " C: for i in xrange(1,10):",
      "*D: for i in xrange(1,11):" ],
    "4": [ "How do you create an if statement with three conditionals in Python?",
      "*A: if a and b and c:",
      " B: if a && b && c:",
      " C: if(a && b && c) {",
      " D: This can't be done in Python" ],
    "5": [
      "How do you make a Python file executable directly in the terminal?",
      " A: Add line '#!/usr/bin/python' at start of file",
      " B: Python files are always executable",
      " C: Create a .pyc file",
      "*D: Add line '#!/usr/bin/python' at start of file and chmod +X file" ]
  }
}

current_quiz = {"name":"python", "question":"1"}

# users
users = {

  # instructor and related
  "drew": { "pwd":"gislason", "access":ACCESS_TEACHER, "token":None, "answer":None },
  "josh": { "pwd":"welschmeyer", "access":ACCESS_STUDENT, "token":None, "answer":None },
  "steve": { "pwd":"dame", "access":ACCESS_STUDENT, "token":None, "answer":None },
  "richard": { "pwd":"ortega", "access":ACCESS_STUDENT, "token":None, "answer":None },
  "me": { "pwd":"pass", "access":ACCESS_STUDENT, "token":None, "answer":None },
  "bryan": { "pwd":"palmer", "access":ACCESS_STUDENT, "token":None, "answer":None },

  # students
  "jonathan": { "pwd":"andress", "access":ACCESS_STUDENT, "token":None, "answer":None },
  "tamer": { "pwd":"awad", "access":ACCESS_STUDENT, "token":None, "answer":None },
  "gareth": { "pwd":"beale", "access":ACCESS_STUDENT, "token":None, "answer":None },
  "dan": { "pwd":"bittner", "access":ACCESS_STUDENT, "token":None, "answer":None },
  "michael": { "pwd":"burgess", "access":ACCESS_STUDENT, "token":None, "answer":None },
  "mark": { "pwd":"byers", "access":ACCESS_STUDENT, "token":None, "answer":None },
  "isaac": { "pwd":"chang", "access":ACCESS_STUDENT, "token":None, "answer":None },
  "victor": { "pwd":"chinn", "access":ACCESS_STUDENT, "token":None, "answer":None },
  "gaurav": { "pwd":"garg", "access":ACCESS_STUDENT, "token":None, "answer":None },
  "thomas": { "pwd":"harvey", "access":ACCESS_STUDENT, "token":None, "answer":None },
  "richard": { "pwd":"hill", "access":ACCESS_STUDENT, "token":None, "answer":None },
  "machael": { "pwd":"messmer", "access":ACCESS_STUDENT, "token":None, "answer":None },
  "dylan": { "pwd":"miller", "access":ACCESS_STUDENT, "token":None, "answer":None },
  "michael": { "pwd":"panciroli", "access":ACCESS_STUDENT, "token":None, "answer":None },
  "thomas": { "pwd":"roome", "access":ACCESS_STUDENT, "token":None, "answer":None },
  "jonathan": { "pwd":"schooler", "access":ACCESS_STUDENT, "token":None, "answer":None },
  "santhosh": { "pwd":"shetty", "access":ACCESS_STUDENT, "token":None, "answer":None },
  "mani": { "pwd":"subramanian", "access":ACCESS_STUDENT, "token":None, "answer":None },
  "joel": { "pwd":"ware", "access":ACCESS_STUDENT, "token":None, "answer":None },
  "dennis": { "pwd":"whetten", "access":ACCESS_STUDENT, "token":None, "answer":None }
}



# ============================ Functions =================================

# return a random N-digit token (defaults to 20 digits)
def QuizToken(N=20):
  return ''.join(random.choice(string.ascii_uppercase + string.ascii_lowercase
    + string.digits) for _ in range(N))

# Returns a username based on token
def QuizLookupUserByToken(token):
  if token == None:
    return None
  token = str(token)
  for username in users:
    if users[username]["token"] == token:
      return username
  return None

# given a quiz object, return the current question (or not started yet)
def QuizGetQuestion(quiz):
  s = '{"question":'
  if quiz["qindex"] == None:
    s = s+'["quiz not started yet"]'
  else:
    question = quiz["questions"][quiz["qindex"]]
    s = s + json.dumps(question)
    i = s.find('*')
    if i >= 0:
      s = s[0:i] + ' ' + s[i+1:]
  s = s+'}'
  return s

# adds a random token to the user and returns the token in JSON form.
def QuizLogin(username):
  global users
  print "QuizLogin: username: " + username
  user = users[username]
  user["token"] = QuizToken()
  return '{"token":"' + user["token"] + '"}\n'

# set a new password
def QuizSetNewPassword(username,newpwd):
  global users
  print "QuizSetNewPassword: username: " + username + " newpwd: " + newpwd
  users[username]["pwd"] = newpwd
  return QuizLogin(username)


# =========================== API Routes =================================


# Allows changing quiz or 
@app.route("/debug", methods=['GET','POST'])
def QuizDebug():
  print "Debugging!\n"
  print "request.get_json:",
  print request.get_json(force=True,silent=True)
  print "request.get_data:",
  print request.get_data()
  print "request.args:",
  print request.args
  token = request.args.get('token')
  print "token: " + str(token)
  print json.dumps(users)

  return "Debugging!\n", 200

# Allows changing quiz or 
@app.route("/api/v1/teacher/admin", methods=['GET', 'POST' ])
def QuizTeacherAdmin():
  print "QuizTeacherAdmin:"

  handled = False
  rsp_data = ""

  # handle get, verify it's a teacher with the token and rights
  if request.method == 'GET':
    if QuizTeacherAccess(request.args.get('token'))
    token = 
    username = QuizLookupUserByToken(token)
    if username and (users[username]["access"] == ACCESS_TEACHER):
      rsp_data = json.dumps(users) + '\n'
      handled = True

  # handle post

  # if handled, it's OK, otherwise, unauthorized
  if handled:
    return rsp_data, 200
  return 401

# allow user to log in
@app.route('/api/v1/login')
@auth.login_required
def QuizApiLogin():
  if auth.username() in users:
    return QuizLogin(auth.username())
  return 401

# allow user to change password
@app.route('/api/v1/profile', methods=['GET', 'POST' ])
@auth.login_required
def QuizApiProfile():
  if auth.username() in users:

    # POST method
    if request.method == 'POST':
      data = request.get_json(force=True,silent=True)
      if data and ("pwd" in data):
        return QuizSetNewPassword(auth.username(), data["pwd"]), 200

    # GET method
    else:
      return QuizLogin(auth.username())

  return 401



# ============================== Main ====================================

if __name__ == "__main__":
    app.debug = True
    app.run(host='0.0.0.0', port=PORT)
#  print "manual testing"
