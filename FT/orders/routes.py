from flask import Blueprint, render_template, url_for, request, flash
from flask_login import login_user, login_required, current_user, logout_user
from FT.models.apartments import Apartments
from FT.models.room import Room
from FT.models.collections import Collections, products_collections
from FT.models.category import Category
from FT.models.apartmenttype import Apartmenttype
from FT.models.products import Products
from FT.models.orders import Orders
from FT.models.projects import Project
from FT.models.orders import Orders, order_statuses, Ordreoversikt, Status
from FT import db
import uuid
from sqlalchemy import func
from FT.forms.webforms import AddOrder
from FT.models.category import products_category


orders = Blueprint('orders', __name__, static_folder="static",
                 template_folder="templates")


# Landingsside for handlekurv
@orders.route('/orders', methods=["GET", "POST"])
@login_required
def order_list():
    standardproducts = {
        "rooms": {}
    }

    #Skjema
    form = AddOrder()

    # Gjeldende leilighet id
    apartment_id = current_user.apartment_id
    # print(apartment_id)

    # Gjeldende leilighet
    apartment = Apartments.query.filter_by(id=apartment_id).first()
    # print(apartment)

    # Ordrer på leiligheten
    apartment_order = Orders.query.filter_by(leilighet_id=apartment_id).all()
    print(apartment_order)

    if not apartment_order:
        print("NO ORDERS")

    # Prosjektet leiligheten er en del av
    project = Project.query.filter_by(id=apartment.project_id).first()
    # print(project)

    # Leilighetstyper til prosjektet
    apartment_types = Apartmenttype.query.filter_by(
        project_id=project.id).all()
    # print(apartment_types)

    # Finn standard-samling i gjeldende prosjekt
    standard_products_collection = []
    for x in apartment_types:
        if x.is_standard:
            standard_products_collection.append(x)

    # Rom i leiligheten
    apartment_rooms = Room.query.filter_by(apartmenttype=apartment_id).all()
    standard_rooms_id = []
    for room in apartment_rooms:
        standard_rooms_id.append(room.id)
    # print("ROM", apartment_rooms)

    # Rom i standardsamling
    standard_apartment_rooms = Room.query.filter_by(
        apartmenttype=standard_products_collection[0].id).all()
    
    # Angi rom-ID-er
    standard_room_id = []

    # Lage rom-objekt
    for room in standard_apartment_rooms:
        standard_room_id.append(room.id)
        standardproducts["rooms"][room.name] = {
            "id": room.id,
            "categories": {}
        }

    # Standardkategorier i leiligheten
    standard_categories = db.session.query(Category).join(Room).filter(
        Category.room_id == Room.id).filter(Room.apartmenttype == standard_products_collection[0].id).all()
    # standard_categories_id = []
    """ for cat in standard_categories:
        standard_categories_id.append(cat.id) """
    # print("STANDARD KATEGORI", standard_categories)

    kategori_rom = db.session.query(Category).join(
        Room).filter(Room.id.in_(standard_room_id)).all()
    # print("CATEGORY-ROOM", kategori_rom)
 
    # Funksjon for å hente produkter basert på kategori-id
    def get_products(cat_ids):
        return Products.query.\
            join(products_category).\
            filter(products_category.columns.category_id.in_(cat_ids)).\
            group_by(Products.nrf).\
            all()

    # Fylle rom-objektet med kategorier og produkter
    for cat in kategori_rom:
        for key in standardproducts["rooms"]:
            # print("key", standardproducts["rooms"][key]["id"])
            if standardproducts["rooms"][key]["id"] == cat.room_id:
                standardproducts["rooms"][key]["categories"][cat.name] = {
                    "id": cat.id,
                        "products": get_products([cat.id])
                }
    
    # Ordrestatus
    test = Status.query.filter_by(id = 1).all()

    print(standardproducts)



    if request.method == "POST":

        for room in standardproducts["rooms"]:
            print(room)
            for category in standardproducts["rooms"][room]["categories"]:
                print(category)
                for product in standardproducts["rooms"][room]["categories"][category]["products"]:
                    print(product.produktnavn)

        """ # Ny ordre og ordreoversikt
        new_order = Orders()

        
        new_order.leilighet_id = apartment_id
        new_order.status = test
        new_order.standardprodukter = 1
        db.session.add(new_order)
        db.session.flush
        db.session.commit()
        db.session.refresh(new_order)
        
        
        # Ordredetaljer
        new_order_details = Ordreoversikt()
        new_order_details.ordre_id = new_order.id
        #produkt_id = db.Column(db.String(100), db.ForeignKey('products.nrf'))
        #antall = db.Column(db.Integer)
        #rom_id = db.Column(db.Integer, db.ForeignKey('room.id'))
        #kategori_id = db.Column(db.Integer, db.ForeignKey('category.id'))
        db.session.add(new_order_details)
        db.session.commit() """
        
        flash("order added")


    return render_template("orders.html", standardproducts=standardproducts, form=form)
