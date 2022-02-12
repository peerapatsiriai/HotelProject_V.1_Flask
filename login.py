from flask import Blueprint
from flask import render_template,request,redirect,url_for,session
from Connect_DB import *
import pymysql
import datetime

# connect database
con = pymysql.connect(HOST,USER,PASSWORD,DATABASE)

loginpage = Blueprint( 'loginpage', __name__)

@loginpage.route("/login")
def login():
   if "username" in session:
      return redirect(url_for('homepage.show_all_room'))
   return render_template("login.html")

@loginpage.route("/checklogin", methods=["POST"]) ## Check Log in
def checklogin():
      username = request.form["username"]
      password = request.form["password"]
      with con:
         cur = con.cursor()
         sql = "SELECT * FROM tb_user WHERE user_username = %s AND user_userpassword = %s"
         cur.execute(sql,(username,password))
         rows = cur.fetchall()
         print(rows)
         # Check user in system
         if len(rows) > 0:
               updatetimelogin_id = rows[0][0]
               updatetimelogin_time = datetime.datetime.now()
               session['username'] = username
               session['userid'] = rows[0][0]
               session['userstatus'] = rows[0][4]
               session['userroom'] = rows[0][3]
               
               # Check User Ban
               if session['userstatus'] <= 0:
                  session.clear()
                  return render_template("login.html",waring="You are banned")
               
               session.permanent = True

               # Update Time stamp when login
               # sql = "update tb_user set usr_timestapm = %s where usr_id = %s"
               # cur.execute(sql,(updatetimelogin_time, updatetimelogin_id))
               cur.close()
               return redirect(url_for('homepage.show_all_room'))
      cur.close()
      return render_template("login.html",waring="Not found user")


@loginpage.route("/logout")
def logout():
   session.clear()
   return render_template("login.html")