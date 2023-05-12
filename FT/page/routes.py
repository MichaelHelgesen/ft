from flask import Blueprint, render_template
from flask_login import login_user, login_required, current_user, logout_user
from FT.models.apartments import Apartments


page = Blueprint('page', __name__, static_folder="static", template_folder="templates")

@page.route('/')
def index():
    if current_user.is_authenticated:
        user_apartments = Apartments.query.filter_by(id = current_user.apartment_id).all()
        return render_template("index.html", name=current_user, user_apartments=user_apartments)
        

    return render_template("index.html", name=current_user)