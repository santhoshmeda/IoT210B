#!/usr/bin/python
# =============================================================================
#        File : QuizStudent.py
# Description : Take Quizical online Quiz
#      Author : Drew Gislsason
#        Date : 3/8/2017
#        Help : QStudent.py [-n]
# =============================================================================
import httplib
import base64
import sys

# ============================== Data =========================================
QUIZICAL_URL  "127.0.0.1:5000"
QSTU_USER     "instructor"
QSTU_PASS     "pass"        # password


# ============================== Login ========================================
def QStuLogin(getNewPass=False):
  newPass1 = Null
  name = raw_input("Enter Username: ")
  pwd  = raw_input("Enter Password: ")
  if getNewPass:
    newPwd1 = raw_input("Enter New Password: ")
    newPwd2 = raw_input("Enter New Password again: ")

  # TODO: save new password to user

  # convert user and password
  userAndPass = name + ":" + pwd
  authorization = "Basic " + base64.b64encode(userAndPass)

  headers = {"Content-type": "application/json",
           "Authorization": authorization}
  conn = httplib.HTTPConnection(QUIZICAL_URL, timeout=5)
  conn.request('GET', '/api/v1/', '{"text":1}', headers)
  r1 = conn.getresponse()
  print "status " + str(r1.status) + ", reason " + str(r1.reason)
  data1 = r1.read()
  print "data: " + str(data1)
  conn.close()

# ============================== Main ====================================
if __name__ == "__main__":
  getNewPwd = False
  if len(argv) >= 2 and argv[1] == "-n":
    getNewPwd = True
  if QStuLogin(getNewPwd) == False:
    QStuLoginFailed()
