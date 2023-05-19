from flask import Blueprint, render_template, url_for
from flask_login import login_user, login_required, current_user, logout_user
from FT.models.apartments import Apartments
from FT.models.room import Room
from FT.models.collections import Collections, products_collections
from FT.models.category import Category
from FT.models.apartmenttype import Apartmenttype
from FT.models.products import Products
from FT import db


user_apartments = Blueprint('user_apartments', __name__, static_folder="static",
                  template_folder="templates")

# Landingsside for alle brukerens leiligheter
@user_apartments.route('/apartment', methods=["GET", "POST"])
@login_required
def apartment_list():
        user_apartments = Apartments.query.filter_by(id = current_user.apartment_id).all()
        return render_template("apartment.html", name=current_user, user_apartments=user_apartments)

@user_apartments.route('/apartment/<string:apartment>', methods=["GET", "POST"])
@login_required
def apartment_rooms(apartment):
        user_apartments = Apartments.query.filter_by(id = current_user.apartment_id).first()
        apartmenttype = db.session.query(Apartmenttype).join(Apartments.apartmenttype).filter(Apartments.id == user_apartments.id).first()
        #print(apartmenttype.name)
        #room_id = Room.query.filter(Room.slug.like(room), Room.apartmenttype.like(apartmenttype_id.id)).first()
        #user_apartmenttype = Apartments.query.filter_by(apartmenttype = user_apartments.apartmenttype).first()
        #test = Apartmenttype.query.join(Apartments.apartmenttype_id).filter(Apartments.id == 1).all()
        #test3 = db.session.query(Products).outerjoin(products_category, Products.nrf == products_category.columns.products_id).filter(products_category.columns.products_id == None).all()
        user_rooms = Room.query.filter_by(apartmenttype = apartmenttype.id).all()
        #print(user_rooms)
        return render_template("apartment_rooms.html", user_rooms=user_rooms, apartment=apartment)

@user_apartments.route('/apartment/<string:apartment>/<string:room>', methods=["GET", "POST"])
@login_required
def apartment_category(apartment, room):
        user_apartments = Apartments.query.filter_by(id = current_user.apartment_id).first()
        apartmenttype = db.session.query(Apartmenttype).join(Apartments.apartmenttype).filter(Apartments.id == user_apartments.id).first()
        room_id = Room.query.filter(Room.name.like(room), Room.apartmenttype.like(apartmenttype.id)).first()
        #print("room id", room_id)
        room_categories = Category.query.filter_by(room_id = room_id.id).all()
        #print(room_categories)
        #room_id = Room.query.filter_by(apartmenttype = )
        
        return render_template("categories.html", apartment=apartment, room=room, categories=room_categories)

@user_apartments.route('/apartment/<string:apartment>/<string:room>/<string:category>', methods=["GET", "POST"])
@login_required
def apartment_product(apartment, room, category):
        user_apartments = Apartments.query.filter_by(id = current_user.apartment_id).first()
        apartmenttype = db.session.query(Apartmenttype).join(Apartments.apartmenttype).filter(Apartments.id == user_apartments.id).first()
        room_id = Room.query.filter(Room.name.like(room), Room.apartmenttype.like(apartmenttype.id)).first()
        category_id = Category.query.filter_by(room_id = room_id.id).first()
        products = Products.query.join(Category.product).filter(Category.id == category_id.id).all()
        #print(category_id)
        #print(room_id)
        return render_template("category_product.html", category=category, room=room, apartment=apartment, products=products)

@user_apartments.route('/apartment/<string:apartment>/<string:room>/<string:category>/<string:product>', methods=["GET", "POST"])
@login_required
def apartment_products(apartment, room, category, product):
        product = Products.query.filter_by(slug = product).first()
        #product = Products.query.filter_by(slug=slug).first()
        product_id = product.nrf
        image_file = url_for('products.static', filename=str(product_id) + ".jpg")
        return render_template("single_product.html", product=product, image_file=image_file)
