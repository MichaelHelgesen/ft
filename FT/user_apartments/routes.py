from flask import Blueprint, render_template, url_for, request, flash, redirect
from flask_login import login_user, login_required, current_user, logout_user
from FT.models.apartments import Apartments, Apartmentdata
from FT.models.room import Room
from FT.models.collections import Collections, products_collections
from FT.models.category import Category
from FT.models.apartmenttype import Apartmenttype
from FT.models.products import Products
from FT.models.cart import Cart
from FT import db, app
import os
from FT.forms import webforms


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
        # Hent leilighetsdata
        user_apartments = Apartments.query.filter_by(id = current_user.apartment_id).first()
        apartment_data = Apartmentdata.query.filter_by(apartment_id = user_apartments.id).all()
        apartmenttype = db.session.query(Apartmenttype).join(Apartments.apartmenttype).filter(Apartments.id == user_apartments.id).first()
        #print(apartmenttype.name)
        #room_id = Room.query.filter(Room.slug.like(room), Room.apartmenttype.like(apartmenttype_id.id)).first()
        #user_apartmenttype = Apartments.query.filter_by(apartmenttype = user_apartments.apartmenttype).first()
        #test = Apartmenttype.query.join(Apartments.apartmenttype_id).filter(Apartments.id == 1).all()
        #test3 = db.session.query(Products).outerjoin(products_category, Products.nrf == products_category.columns.products_id).filter(products_category.columns.products_id == None).all()
        user_rooms = Room.query.filter_by(apartmenttype = apartmenttype.id).all()
        print(user_rooms)
        print(user_apartments.id)
        return render_template("apartment_rooms.html", user_rooms=user_rooms, apartment=apartment, apartmentdata=apartment_data)

@user_apartments.route('/apartment/<string:apartment>/<string:room>', methods=["GET", "POST"])
@login_required
def apartment_category(apartment, room):
        file_form = webforms.FileUpload()
        user_apartments = Apartments.query.filter_by(id = current_user.apartment_id).first()
        apartmenttype = db.session.query(Apartmenttype).join(Apartments.apartmenttype).filter(Apartments.id == user_apartments.id).first()
        room_id = Room.query.filter(Room.name.like(room), Room.apartmenttype.like(apartmenttype.id)).first()
        #print("room id", room_id)
        room_categories = Category.query.filter_by(room_id = room_id.id).all()
        #print(room_categories)
        #room_id = Room.query.filter_by(apartmenttype = )
        #username = current_user.name.strip().capitalize()
        user_folder = os.path.join(app.config['UPLOAD_PATH'], user_apartments.apartment_id, room)
        files = None
        
        if request.method == "POST":
                if not os.path.isdir(user_folder):
                        os.mkdir(user_folder)
                files = os.listdir(os.path.join(app.config['UPLOAD_PATH'], user_apartments.apartment_id, room))
                if file_form.fileSubmit.data:
                        uploaded_file = request.files['file']
                        if uploaded_file.filename != '':
                                #uploaded_file.save(uploaded_file.filename)
                                uploaded_file.save(os.path.join(app.config['UPLOAD_PATH'], user_apartments.apartment_id, room, uploaded_file.filename))
                flash("uploaded")
                return redirect(request.url)

        return render_template("categories.html", user_folder=user_folder, username=user_apartments.apartment_id, files=files, file_form=file_form, room_id=room_id, apartment=apartment, room=room, categories=room_categories)

@user_apartments.route('/apartment/<string:apartment>/<string:room>/<string:category>', methods=["GET", "POST"])
@login_required
def apartment_product(apartment, room, category):
        user_apartments = Apartments.query.filter_by(id = current_user.apartment_id).first()
        apartmenttype = db.session.query(Apartmenttype).join(Apartments.apartmenttype).filter(Apartments.id == user_apartments.id).first()
        room_id = Room.query.filter(Room.name.like(room), Room.apartmenttype.like(apartmenttype.id)).first()
        #category_id = Category.query.filter_by(room_id = room_id.id).first()
        category_id = Category.query.filter(Category.name.like(category), Room.apartmenttype.like(apartmenttype.id)).first()
        products = Products.query.join(Category.product).filter(Category.id == category_id.id).all()
        #print(category_id2)
        #print(room_id)
        print(products)
        print(category_id.id)
        return render_template("category_product.html", category=category, room=room, apartment=apartment, products=products)

@user_apartments.route('/apartment/<string:apartment>/<string:room>/<string:category>/<string:product>', methods=["GET", "POST"])
@login_required
def apartment_products(apartment, room, category, product):
        form = webforms.AddToCart()
        product = Products.query.filter_by(slug = product).first()
        apartment = Apartments.query.filter_by(apartment_id = apartment).first()
        apartmenttype = db.session.query(Apartmenttype).join(Apartments.apartmenttype).filter(Apartments.id == apartment.id).first()
        room_id = Room.query.filter(Room.name.like(room), Room.apartmenttype.like(apartmenttype.id)).first()
        category_id = db.session.query(Category).join(Room).filter(Category.name == category).filter(Room.apartmenttype == apartmenttype.id).first()
        #category_id = Category.query.filter(Category.name.like(category), Room.apartmenttype.like(apartmenttype.id)).first()
        product_id = product.nrf
        image_file = url_for('products.static', filename=str(product_id) + ".jpg")

        category_apartmentdata = category_id.apartment_data
        
        apartment_data_value = Apartmentdata.query.filter_by(apartment_id=apartment.id, datatype=category_apartmentdata).first()
        
        print("ROM", room)
        print("ROM-ID", room_id.id)
        print("APARTMENT-ID", apartment.id)
        print("APARTMENTTYPE", apartmenttype.id)
        print("CATEGORY", category)
        print("CATEGORY ID", category_id)
        print(category_apartmentdata)
        
        print(apartment_data_value)
        

        if request.method == "POST":
                cart = Cart()
                cart.leilighet_id = apartment.id
                cart.produkt_id = product.nrf
                cart.antall = apartment_data_value.verdi
                cart.rom = room_id.id
                cart.kategori = category_id.id
                db.session.add(cart)
                db.session.commit()
                flash("added to cart")

        return render_template("single_product.html", apartment_data_value=apartment_data_value, product=product, form=form, image_file=image_file, apartment=apartment, room=room, category=category)


