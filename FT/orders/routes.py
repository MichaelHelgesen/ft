from flask import Blueprint, render_template, url_for
from flask_login import login_user, login_required, current_user, logout_user
from FT.models.apartments import Apartments
from FT.models.room import Room
from FT.models.collections import Collections, products_collections
from FT.models.category import Category
from FT.models.apartmenttype import Apartmenttype
from FT.models.products import Products
from FT import db



orders = Blueprint('orders', __name__, static_folder="static",
                  template_folder="templates")


# Landingsside for ordrer
@orders.route('/orders', methods=["GET", "POST"])
@login_required
def order_list():
    return render_template("orders.html")
