from flask import Blueprint, render_template, request
from FT.forms import webforms

login = Blueprint('login', __name__, static_folder="static", template_folder="templates")
forgot_password = Blueprint('forgot_password', __name__)



@login.route('/login', methods=["GET", "POST"])
def user_login():
    form = webforms.MyForm()
    name = None
    if form.validate_on_submit():
        name = form.name.data
        form.name.data = ""
        return render_template("user_login.html", form=form, name=name)
    else:
        return render_template("user_login.html", form=form)

@forgot_password.route('/forgot_password')
def user_password():
    return render_template("user_password.html")
