from flask import Blueprint
from flask import render_template,request,redirect,url_for,session
from Connect_DB import *
import pymysql
import datetime as dt

# connect database
con = pymysql.connect(HOST,USER,PASSWORD,DATABASE)

homepage = Blueprint( 'homepage', __name__)

@homepage.route("/homepage")
def show_all_room():
     if "username" not in session:
          return render_template("login.html", waring ="You are not Login")
     with con:
          cur = con.cursor()
          sql = "SELECT * FROM tb_rooms"
          cur.execute(sql)
          data = cur.fetchall()
     return render_template("homepage.html",rooms = data)


@homepage.route("/room", methods=['POST'])
def showroom():
     if "username" not in session:
          return render_template("login.html", waring ="You are not Login")
     data = request.form['id']
     user_id = session['userid']
     with con:
          cur = con.cursor()
          sql = "SELECT * FROM tb_rooms where room_id = %s"
          cur.execute(sql,data)
          data_room = cur.fetchall()     
          sql = "SELECT * FROM tb_user where user_id = %s"
          cur.execute(sql,user_id)
          data_user = cur.fetchall()  
          user_have_room = data_user[0][3]
          # session['userroom'] = "xx"  
     return render_template("single_room.html",room = data_room,user_have_room = user_have_room)

@homepage.route("/bookroom", methods=['POST'])
def bookroom():
     roomid = request.form['id']
     username = session["username"]
     userid = session['userid']
     with con:
          cur = con.cursor()
          sql = "INSERT INTO tb_confirm (user_id, user_name, room_id) VALUES (%s, %s, %s);"
          cur.execute(sql,(userid,username,roomid))
          sql = "update tb_user set user_room = %s where user_id = %s "
          word = "wait"
          cur.execute(sql,(word,userid))
          session['userroom'] = "xx"
     return redirect(url_for('homepage.show_all_room'))

@homepage.route("/myroom")
def showmyroom():
     if "username" not in session:
          return render_template("login.html", waring ="You are not Login")
     
     with con:
          cur = con.cursor()
          sql = "SELECT * FROM tb_user where user_id = %s"
          cur.execute(sql,session['userid'])
          member = cur.fetchall()

          check_user_room = member[0][3]
          
          if check_user_room == "x":
               return redirect(url_for('homepage.show_all_room'))
          if check_user_room == "wait":
               return render_template('wait.html')

          sql = "SELECT * FROM tb_rooms where room_id = %s"
          room_id = member[0][3]
          cur.execute(sql,room_id)
          data = cur.fetchall()
          # select date
          sql = "SELECT * FROM tb_user_status where user_room = %s"
          cur.execute(sql,room_id)
          date = cur.fetchall()   
          day_limit = date[0][1]
          day_now = dt.datetime.now()
          time = day_now - day_limit
          result = time.days
          # check day late 
          if result < 0:
               result = result * -1
               status =  str(result) + " Day To Pay"
          elif result == 0:
               status = "To Day"
          else:
               status = "You Late " + str(result) + " Day"
     day_limit = date[0][1].strftime('%Y-%m-%d')
     last_pay=date[0][2].strftime('%Y-%m-%d')
     return render_template("myroom.html",room = data, day_limit = day_limit, last_pay = last_pay, status = status)

# @homepage.route("/cencle",methods=['POST'])
# def cancle():
#      session['userroom'] = "x"
#      roomid = request.form['id']
#      user = session['userid']
#      with con:
#           cur = con.cursor()
#           sql = "update tb_user set user_room = %s where user_id = %s "
#           cur.execute(sql,("x",user))
#           sql = "update tb_rooms set room_status = 0  where room_id = %s "
#           cur.execute(sql,roomid)
#           sql = "update tb_rooms set room_owner = 0 where room_id = %s "
#           cur.execute(sql,roomid)
#           sql = "DELETE FROM tb_user_status WHERE user_id= %s;"
#           cur.execute(sql,user)        
#      print(session)
#      return redirect(url_for('homepage.show_all_room'))  

@homepage.route("/floor1")
def showroom_floor1():
     if "username" not in session:
          return render_template("login.html", waring ="You are not Login")
     with con:
          cur = con.cursor()
          sql = "SELECT * FROM tb_rooms where room_floor = 1"
          cur.execute(sql)
          data = cur.fetchall()
     return render_template("room_floor.html",rooms = data, floor = 1)

@homepage.route("/floor2")
def showroom_floor2():
     if "username" not in session:
          return render_template("login.html", waring ="You are not Login")
     with con:
          cur = con.cursor()
          sql = "SELECT * FROM tb_rooms where room_floor = 2"
          cur.execute(sql)
          data = cur.fetchall()
     return render_template("room_floor.html",rooms = data, floor = 2)

@homepage.route("/floor3")
def showroom_floor3():
     if "username" not in session:
          return render_template("login.html", waring ="You are not Login")
     with con:
          cur = con.cursor()
          sql = "SELECT * FROM tb_rooms where room_floor = 3"
          cur.execute(sql)
          data = cur.fetchall()
     return render_template("room_floor.html",rooms = data, floor = 3)