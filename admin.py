from flask import Blueprint
from flask import render_template,request,redirect,url_for,session
from Connect_DB import *
import pymysql
import datetime as dt

con = pymysql.connect(HOST,USER,PASSWORD,DATABASE)

page_admin = Blueprint( 'page_admin', __name__)

@page_admin.route("/admin")
def adminpage():
    if "username" not in session:
        return render_template("login.html", waring ="You are not Login")
    if session['userstatus'] != 2:
        return redirect(url_for('homepage.show_all_room'))
    with con:
        cur = con.cursor()
        sql = "SELECT * FROM tb_confirm"
        cur.execute(sql)
        data= cur.fetchall()
        print(data)
    return render_template("admin.html", data = data)

@page_admin.route("/confirm")
def confirm():
    if "username" not in session:
        return render_template("login.html", waring ="You are not Login")
    if session['userstatus'] != 2:
        return redirect(url_for('homepage.show_all_room'))
    with con:
        cur = con.cursor()
        sql = "SELECT * FROM tb_confirm"
        cur.execute(sql)
        data = cur.fetchall()
    return render_template("confirm.html",datas = data)

@page_admin.route("/confirmpay")
def confirmpay():
    if "username" not in session:
        return render_template("login.html", waring ="You are not Login")
    if session['userstatus'] != 2:
        return redirect(url_for('homepage.show_all_room'))
    with con:
        cur = con.cursor()
        sql = "SELECT tb_user.user_id, tb_user.user_username, tb_user.user_room, tb_user_status.user_daypay, tb_user_status.user_daylimit FROM tb_user INNER JOIN tb_user_status ON tb_user.user_id = tb_user_status.user_id;"
        cur.execute(sql)
        data = cur.fetchall()
        # sql = "SELECT * FROM tb_user_status ORDER BY user_id"
        # cur.execute(sql)
        # user_date = cur.fetchall()
    return render_template("confirmpay.html",data = data)

@page_admin.route("/deleteconfirm", methods = ["POST"])
def deleteconfirm():
    with con:
        id_user = request.form["id"]
        print(id_user)
        cur = con.cursor()
        sql = "DELETE FROM tb_confirm WHERE user_id = %s"
        cur.execute(sql,id_user)
        sql = "update tb_user set user_room = %s where user_id = %s "
        cur.execute(sql,("x",id_user))
    return redirect(url_for('page_admin.confirm'))

@page_admin.route("/confirm_room", methods = ["POST"])
def confirmroom():
    with con:
        id_user = request.form["id"]
        roomid = request.form["room_id"]
        cur = con.cursor()
        sql = "DELETE FROM tb_confirm WHERE user_id = %s"
        cur.execute(sql,id_user)
        sql = "update tb_user set user_room = %s where user_id = %s "
        cur.execute(sql,(roomid,id_user))
        sql = "update tb_rooms set room_status = 1  where room_id = %s "
        cur.execute(sql,roomid)
        sql = "update tb_rooms set room_owner = %s where room_id = %s "
        cur.execute(sql,(id_user,roomid))
        # Insert date time
        day_now = dt.datetime.now()
        day_limlt = day_now + dt.timedelta(days=30)
        sql = "INSERT INTO tb_user_status  (user_id,user_daylimit,user_daypay,user_room)  VALUES (%s, %s, %s, %s) "
        cur.execute(sql,(id_user,day_limlt,day_now,roomid))  
    return redirect(url_for('page_admin.confirm'))

@page_admin.route("/confirmpaysuccess", methods=["POST"])
def confirmpaysuccess():
    with con:
        user_id = request.form["id"]
        cur = con.cursor()
        sql = "SELECT user_daylimit FROM tb_user_status WHERE user_id = %s "
        cur.execute(sql,user_id)
        date = cur.fetchall()
        ##### update datetime to DB
        day_now = dt.datetime.now()
        day_limlt = date[0][0] + dt.timedelta(days=30)
        sql = "update tb_user_status set user_daylimit = %s where user_id = %s"
        cur.execute(sql,(day_limlt,user_id))
        sql = "update tb_user_status set user_daypay = %s where user_id = %s"
        cur.execute(sql,(day_now, user_id))
        return redirect(url_for('page_admin.confirmpay'))

@page_admin.route("/cencleroom")
def cencleroom():
    if "username" not in session:
        return render_template("login.html", waring ="You are not Login")
    if session['userstatus'] != 2:
        return redirect(url_for('homepage.show_all_room'))
    with con:
        cur = con.cursor()
        sql = "SELECT tb_user.user_id, tb_user.user_username, tb_user.user_room, tb_user_status.user_daypay, tb_user_status.user_daylimit FROM tb_user INNER JOIN tb_user_status ON tb_user.user_id = tb_user_status.user_id;"
        cur.execute(sql)
        data = cur.fetchall()
    return render_template("cancle.html",datas = data)

@page_admin.route("/cencle",methods=['POST'])
def cancle():
    roomid = request.form['room_id']
    user = request.form['id']
    print(user)
    print(roomid)
    with con:
        cur = con.cursor()
        sql = "update tb_user set user_room = %s where user_id = %s "
        cur.execute(sql,("x",user))
        sql = "update tb_rooms set room_status = 0  where room_id = %s "
        cur.execute(sql,roomid)
        sql = "update tb_rooms set room_owner = 0 where room_id = %s "
        cur.execute(sql,roomid)
        sql = "DELETE FROM tb_user_status WHERE user_id= %s;"
        cur.execute(sql,user) 
    # print(session)
    return redirect(url_for('homepage.show_all_room'))  

@page_admin.route("/banpage")
def ban():
    with con:
        if "username" not in session:
            return render_template("login.html", waring ="You are not Login")
        if session['userstatus'] != 2:
            return redirect(url_for('homepage.show_all_room'))
        cur = con.cursor()
        sql = "SELECT * FROM tb_user"
        cur.execute(sql)
        users = cur.fetchall()
        return render_template('ban.html',datas = users)

@page_admin.route("/banuser", methods=["POST"])
def ban_user():
    user_id = request.form["id"]
    with con:
        cur = con.cursor()
        sql = "update tb_user set user_status = 0 where user_id = %s"
        cur.execute(sql,user_id)
        return redirect(url_for('page_admin.ban'))

@page_admin.route("/unbanuser", methods=["POST"])
def unban_user():
    user_id = request.form["id"]
    with con:
        cur = con.cursor()
        sql = "update tb_user set user_status = 1 where user_id = %s"
        cur.execute(sql,user_id)
        return redirect(url_for('page_admin.ban'))

@page_admin.route("/editroom")
def editroom():
    with con:
        cur = con.cursor()
        sql = "SELECT * FROM tb_user_status"
        cur.execute(sql)
        data = cur.fetchall()
        return render_template('editroom.html',datas = data)

@page_admin.route("/editroom_post", methods=["POST"])
def editroom_post():
    if "username" not in session:
        return render_template("login.html", waring ="You are not Login")
    if session['userstatus'] != 2:
        return redirect(url_for('homepage.show_all_room'))

    lastpay = request.form['lastpay']
    limit = request.form['limit']
    room_id = request.form['id']
    with con:  
        cur = con.cursor()
        sql = "update tb_user_status set user_daylimit = %s where user_id = %s"
        cur.execute(sql,(limit,room_id))
        sql = "update tb_user_status set user_daypay = %s where user_id = %s"
        cur.execute(sql,(lastpay,room_id))
    return redirect(url_for('page_admin.editroom'))