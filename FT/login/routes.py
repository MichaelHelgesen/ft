from flask import Blueprint, render_template, flash
from FT.forms import webforms
from FT import db
from FT.models.add_user import Users
from werkzeug.security import generate_password_hash, check_password_hash

login = Blueprint('login', __name__, static_folder="static", template_folder="templates")

@login.route('/login', methods=["GET", "POST"])
def user_login():
    form = webforms.LoginForm()
    name = None
    if form.validate_on_submit():
        user = Users.query.filter_by(email=form.email.data).first()
        if user is None:
            flash("Username or password is wrong")
            return render_template("user_login.html", form=form)
        else:
            if check_password_hash(user.password_hash, form.password.data):
                name = user.name
                form.email.data = ""
                print(form)
                return render_template("user_login.html", form=form, name=name)
            else:
                flash("Password is wrong")
                form.email.data = ""
                form.password.data = ""
                return render_template("user_login.html", form=form)
    else:
        return render_template("user_login.html", form=form)

@login.route("/register", methods=["GET", "POST"])
def user_register():
    form = webforms.UserForm()
    if form.validate_on_submit():
        user = Users.query.filter_by(email=form.email.data).first()
        if user is None:
            user = Users(
                name=form.name.data,
                email=form.email.data,
                username=form.username.data,
                password_hash=generate_password_hash(form.password_hash.data, method="sha256"),
            )
            db.session.add(user)
            db.session.commit()
            flash("Bruker lagret")
            form.name.data = ""
            form.email.data = ""
            form.username.data = ""
            form.password_hash.data = ""
            return render_template("user_register.html", form=form)
        else:
            flash("Denne eposten er allerede registrert")
            form.name.data = ""
            return render_template("user_register.html", form=form)
    else:
        return render_template("user_register.html", form=form)
