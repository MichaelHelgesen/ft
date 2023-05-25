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
    standardproducts = {}

    # Gjeldende leilighet id
    apartment_id = current_user.apartment_id
    #print(apartment_id)
    
    #Gjeldende leilighet
    apartment = Apartments.query.filter_by(id = apartment_id).first()
    #print(apartment)

    #Ordrer på leiligheten
    apartment_order = Orders.query.filter_by(leilighet_id = apartment_id).first()
    #print(apartment_order)

    #Prosjektet leiligheten er en del av
    project = Project.query.filter_by(id = apartment.project_id).first()
    #print(project)

    #Leilighetstyper til prosjektet
    apartment_types = Apartmenttype.query.filter_by(project_id = project.id).all()
    #print(apartment_types)
    
    # Finn standard-samling i gjeldende prosjekt
    standard_products_collection = []
    for x in apartment_types:
        if x.is_standard:
            standard_products_collection.append(x);
    
    #Rom i leiligheten
    apartment_rooms = Room.query.filter_by(apartmenttype = apartment_id).all()
    standard_rooms_id = []
    for room in apartment_rooms:
        standard_rooms_id.append(room.id)
    #print("ROM", apartment_rooms)

    #Rom i standardsamling
    standard_apartment_rooms = Room.query.filter_by(apartmenttype = standard_products_collection[0].id).all()
    standard_room_id = []
    for room in standard_apartment_rooms:
        standard_room_id.append(room.id)
        standardproducts[room.name] = {
            "id":room.id
        }
    #print("STANDARDROM", standard_apartment_rooms)
           
    # Standardkategorier i leiligheten
    standard_categories = db.session.query(Category).join(Room).filter(Category.room_id == Room.id).filter(Room.apartmenttype == standard_products_collection[0].id).all()
    #standard_categories_id = []
    """ for cat in standard_categories:
        standard_categories_id.append(cat.id) """
    #print("STANDARD KATEGORI", standard_categories)

    kategori_rom = db.session.query(Category).join(Room).filter(Room.id.in_(standard_room_id)).all()
    #print("CATEGORY-ROOM", kategori_rom)

    def get_products(cat_ids):
        return Products.query.\
            join(products_category).\
            filter(products_category.columns.category_id.in_(cat_ids)).\
            group_by(Products.nrf).\
            all()


    for cat in kategori_rom:
        for key in standardproducts:
            if standardproducts[key]["id"] == cat.room_id:
                standardproducts[key][cat.name] = {
                    "id":cat.id,
                    "products":get_products([cat.id])
                }
                #standardproducts[key][cat.name]["products"].append(get_products([cat.id]))

    standard_categories_ids = []
    for x in standard_categories:
        standard_categories_ids.append(x.id)
    #standard_products = db.session.query
    #db.session.query(Products).outerjoin(products_category, Products.nrf == products_category.columns.products_id).filter(products_category.columns.category_id == None).all()
    #test = Products.query.join(Category.room_id).filter_by(room_id=1).all()
    #print(test)

    objekt = {
        "stue": {
            "parkett": [1, 2, 3],
            "flis": [1,2,3]
        },
        "gang": {
            "listverk": [1,2,3]
        }
    }


    def get_skilled_candidates(cat_ids):
        return Products.query.\
            join(products_category).\
            filter(products_category.columns.category_id.in_(cat_ids)).\
            group_by(Products.nrf).\
            all()
    
    standardprodukter = get_skilled_candidates(standard_categories_ids)

    for prod in standardprodukter:
        print(prod.produktnavn)
        for key in standardproducts:
            print(standardproducts[key]["id"])
            for y in standardproducts[key]:
                print(standardproducts[key][y])


    print("STANDARDPRODUKTER", standardproducts)

    return render_template("cart.html", standardproducts=standardproducts)
