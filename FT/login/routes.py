from flask import Blueprint, render_template, flash, redirect, url_for, request, jsonify
from FT.forms import webforms
from FT import db, app
import flask_excel as excel
import io
import pandas as pd
from FT.models.add_user import Users, Role
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, login_required, current_user, logout_user
import csv
login = Blueprint('login', __name__, static_folder="static",
                  template_folder="templates")


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
                login_user(user, remember=True)
                return render_template("profile.html", name=name)
            else:
                flash("Password is wrong")
                form.email.data = ""
                form.password.data = ""
                return render_template("user_login.html", form=form)
    else:
        return render_template("user_login.html", form=form)


@login.route("/register", methods=["GET", "POST"])
# @login_required
def user_register():
    form = webforms.UserForm()
    if form.validate_on_submit():
        user = Users.query.filter_by(email=form.email.data).first()
        if user is None:
            user = Users(
                name=form.name.data,
                email=form.email.data,
                username=form.username.data,
                password_hash=generate_password_hash(
                    form.password_hash.data, method="sha256"),
            )
            user.role.append(Role.query.filter_by(name="user").first())
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


@login.route('/profile')
@login_required
def user_profile():
    return render_template("profile.html", name=current_user.name)


@login.route('/logout')
@login_required
def user_logout():
    logout_user()
    return redirect(url_for("page.index"))


@login.route("/users", methods=["GET", "POST"])
@login_required
def admin_users():
    form = webforms.ImportForm()
    users = Users.query.all()
    user_role = Role.query.filter_by(name="user").first()
    if request.method == "POST":
        #df = pd.read_csv(request.files.get('file'))
        df = pd.read_excel(request.files.get('file'))
        #print(df)
        
        for index in df.index:
            check_user = Users.query.filter_by(email = df["email"][index]).first()
            if check_user is None:
                user = Users()
                user.name = df["name"][index]
                user.email = df["email"][index]
                user.username = df["username"][index]
                user.role = [user_role]
                db.session.add(user)
                db.session.commit()
                users = Users.query.all()
        flash("imported")
        return render_template('users.html', users=users, form=form)
       
    return render_template("users.html", users=users, form=form)


@login.route("/upload")
@login_required
def admin_import():
    users = Users.query.all()
    return render_template("upload.html")


@login.route("/users/<int:id>", methods=["GET", "POST"])
@login_required
def admin_user_update(id):
    user = Users.query.get_or_404(id)
    form = webforms.UpdateUserForm()
    if request.method == "POST":
        password = request.form["password_hash"]
        if password:
            hashed_pw = generate_password_hash(password, "sha256")
            user.password_hash = hashed_pw
            user.name = request.form["name"]
            user.email = request.form["email"]
            user.username = request.form["username"]
        try:
            db.session.commit()
            flash("User updated!")
            return render_template("update_user.html", form=form, user=user)
        except:
            flash("Error")
            return render_template("update_user.html", form=form, user=user)
    else:
        return render_template("update_user.html", form=form, user=user)

@login.route('/download', methods=['GET'])
def download_data():
    users = Users.query.all()
    print(users)
    user_id = []
    user_names = []
    user_emails = []
    user_username = []
    for users in users:
        user_id.append(users.id)
        user_names.append(users.name)
        user_emails.append(users.email)
        user_username.append(users.username)
        print(users.role)
    excel.init_excel(app)
    extension_type = "xls"
    filename = "test123" + "." + extension_type
    d = {'id': user_id, "name": user_names, "email": user_emails, "username": user_username}
    return excel.make_response_from_dict(d, file_type=extension_type, file_name=filename)

@login.route('/import', methods=["GET", 'POST'])
def import_data():
    print("import")
    flash("updated")
    return redirect(url_for("login.admin_users"))


