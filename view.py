from flask import Flask
from flask import render_template,session
from login import *
from home import *
from admin import *
from register import *
from datetime import timedelta


app = Flask(__name__)

# key for encoding
app.secret_key = "Ez"

# time in system
app.permanent_session_lifetime = timedelta(hours=2)

# register all page
# app.register_blueprint(memberpage)
# app.register_blueprint(loginpage)
app.register_blueprint(registerpage)
app.register_blueprint(loginpage)
app.register_blueprint(homepage)
app.register_blueprint(page_admin)

# first page
@app.route("/")
def login():
     return render_template("welcome.html")


if __name__ == '__main__':
    app.run(debug=True)
