from flask import Blueprint
from flask import render_template,request,redirect,url_for
from Connect_DB import *
import  datetime as dt
import pymysql

# connect database
con = pymysql.connect(HOST,USER,PASSWORD,DATABASE)

registerpage = Blueprint( 'registerpage', __name__)

@registerpage.route("/register")
def register():
     return render_template("register.html")

@registerpage.route("/registepager", methods=["POST"])
def checkregister():
    if request.method == "POST":

        username = request.form["username"]
        password = request.form["userpass"]
        phone = request.form["phone"]
        email = request.form["email"]

        with con:
            cur = con.cursor()
            sql = "INSERT INTO tb_user (user_username, user_userpassword, user_phone, user_email) VALUES ( %s, %s, %s, %s);"
            cur.execute(sql,(username, password, phone, email))
            return render_template("login.html")
