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



cart = Blueprint('cart', __name__, static_folder="static",
                  template_folder="templates")


# Landingsside for handlekurv
@cart.route('/cart', methods=["GET", "POST"])
@login_required
def cart_list():
    apartment_id = current_user.apartment_id
    print(apartment_id)
    apartment = Apartments.query.filter_by(id = apartment_id).first()
    print(apartment)
    apartment_order = Orders.query.filter_by(leilighet_id = apartment_id).first()
    print(apartment_order)
    project = Project.query.filter_by(id = apartment.project_id).first()
    print(project)
    apartment_types = Apartmenttype.query.filter_by(project_id = project.id).all()
    print(apartment_types)
    standard_products_collection = []
    for x in apartment_types:
        if x.is_standard:
            standard_products_collection.append(x);
    print(standard_products_collection[0])
    print(standard_products_collection[0].id)
    standard_rooms = Room.query.filter_by(apartmenttype = apartment_id).all()
    print(standard_rooms)       
    standard_categories = db.session.query(Category).join(Room).filter(Category.room_id == Room.id).filter(Room.apartmenttype == standard_products_collection[0].id).all()
    print(standard_categories)
    #standard_products = db.session.query


    return render_template("cart.html")
