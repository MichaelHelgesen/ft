from flask import Blueprint, render_template, url_for
from flask_login import login_user, login_required, current_user, logout_user
from FT.models.apartments import Apartments
from FT.models.room import Room
from FT.models.collections import Collections, products_collections
from FT.models.category import Category
from FT.models.apartmenttype import Apartmenttype
from FT.models.products import Products
from FT.models.orders import Orders
from FT.models.projects import Project
from FT import db
from FT.models.category import products_category


cart = Blueprint('cart', __name__, static_folder="static",
                 template_folder="templates")


# Landingsside for handlekurv
@cart.route('/cart', methods=["GET", "POST"])
@login_required
def cart_list():


    return render_template("cart.html")
