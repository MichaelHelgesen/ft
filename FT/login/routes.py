from flask import Blueprint, render_template

login = Blueprint('login', __name__, static_folder="static", template_folder="templates")
forgot_password = Blueprint('forgot_password', __name__)

@login.route('/login')
def user_login():
    return render_template("user_login.html")

@forgot_password.route('/forgot_password')
def user_password():
    return render_template("user_password.html")
