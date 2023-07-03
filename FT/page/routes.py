from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_user, login_required, current_user, logout_user
from FT.models.apartments import Apartments
from FT.models.add_user import Users
from FT.models.add_user import Role
from FT.models.add_user import apartments_users
from FT.forms import webforms
from FT import db


page = Blueprint('page', __name__, static_folder="static", template_folder="templates")

@page.route('/')
def index():
    if current_user.is_authenticated:
        print(current_user.apartments)
        user_apartments = Apartments.query.filter_by(id = current_user.apartment_id).all()
        user_apartment_list = db.session.query(Apartments).join(apartments_users).filter(apartments_users.columns.user_id == current_user.id).all()
        return render_template("index.html", name=current_user, user_apartments=user_apartments, user_apartment_list=user_apartment_list)
    return render_template("index.html", name=current_user)

@page.route('/modal', methods=["GET", "POST"])
def index_modal():
    form = webforms.SelectApartment("")
    user_apartments = db.session.query(Apartments).join(apartments_users).filter(apartments_users.columns.user_id == current_user.id).all()
    #form.apartments.process([])
   
    return render_template("apartment-list.html", user_apartments=user_apartments, form=form)

@page.route('/modal2', methods=["GET", "POST"])
def index_modal2():
    form = webforms.SelectApartment("")
    user_form = webforms.UpdateUserForm
    user = Users.query.get_or_404(current_user.id)
    roles = Role.query.all()
    if request.method == "POST":
        selected_id = request.form["selected_apartment"]
        user_apartments = Apartments.query.filter_by(id = selected_id).first()
        print(user_apartments)
        print(current_user.apartment_id)
        user.apartment_id = selected_id
        print(user)
        db.session.commit()
        flash("User updated!")
        if "shop" in request.referrer:
            return redirect(url_for("user_apartments.apartment_rooms", apartment=selected_id))
        return redirect(request.referrer)
    if request.method == "GET":
        print("get")
        print(request.referrer)
        return redirect(request.referrer)
    