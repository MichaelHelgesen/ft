from flask import Blueprint, render_template, url_for, request, flash, redirect
from flask_login import login_user, login_required, current_user, logout_user
from FT.models.apartments import Apartments, Apartmentdata
from FT.models.room import Room
from FT.models.collections import Collections, products_collections
from FT.models.category import Category
from FT.models.apartmenttype import Apartmenttype
from FT.models.products import Products
from FT.models.orders import Orders, Status
from FT.models.projects import Project
from FT.models.orders import Orders, order_statuses, Ordreoversikt, Status
from FT import db, app
from FT.models.add_user import Users
import flask_excel as excel
import pandas as pd
import sqlite3
import uuid
import os
from sqlalchemy import func
from FT.forms.webforms import AddOrder, DeleteOrder, ChangeStatus
from FT.models.category import products_category


orders = Blueprint('orders', __name__, static_folder="static",
                 template_folder="templates")


# Landingsside for handlekurv
@orders.route('/orders', methods=["GET", "POST"])
@login_required
def order_list():

    standardproducts = {
        "rooms": {},
        "totalPrice": 0,
        "status": "d"
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
    apartment_order = Orders.query.filter_by(leilighet_id=apartment_id, standardprodukter=0).all()
    print(apartment_order)

    # Standardordrer på leiligheten
    standard_apartment_order = Orders.query.filter_by(leilighet_id=apartment_id, standardprodukter=1).all()
    #print("standard", standard_apartment_order)

    # Prosjektet leiligheten er en del av
    project = Project.query.filter_by(id=apartment.project_id).first()
    # print(project)

    # Leilighetstyper til prosjektet
    apartment_types = Apartmenttype.query.filter_by(
        project_id=project.id).all()
    print("apartment_types", apartment_types)

    # Finn standard-samling i gjeldende prosjekt
    standard_products_collection = []
    for x in apartment_types:
        if x.is_standard:
            standard_products_collection.append(x)
    print ("STANDARD", standard_products_collection)
    
    # Rom i leiligheten
    apartment_rooms = Room.query.filter_by(apartmenttype=apartment_id).all()
    if apartment_rooms:
        standard_rooms_id = []
        for room in apartment_rooms:
            standard_rooms_id.append(room.id)
        print("ROM", apartment_rooms)

        # Rom i standardsamling
        standard_apartment_rooms = Room.query.filter_by(
            apartmenttype=standard_products_collection[0].id).all()
        print("standardroms", standard_apartment_rooms)
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


        #Fylle rom-objektet med kategorier og produkter
        for cat in kategori_rom:
            print(cat.apartment_data)
            antall = Apartmentdata.query.filter(Apartmentdata.datatype == cat.apartment_data, Apartmentdata.apartment_id == apartment_id).first()
            print("ANTALL", antall)
            for key in standardproducts["rooms"]:
                # print("key", standardproducts["rooms"][key]["id"])
                if standardproducts["rooms"][key]["id"] == cat.room_id:
                    standardproducts["rooms"][key]["categories"][cat.name] = {
                        "id": cat.id,
                        "products": []
                    }
                    stand_prod = get_products([cat.id])
                    for prod in stand_prod:
                        standardproducts["rooms"][key]["categories"][cat.name]["products"].append({
                            "product": prod,
                            "price": prod.pris,
                            "num": antall.verdi
                        })
        
        # Ordrestatus
        test = Status.query.filter_by(id = 2).first()
        print("TEST", test.name)
        
        

        if not standard_apartment_order and not apartment_order:
            standardproducts["status"] = test.name
            for x in current_user.role:
                if x.name == "user":
                    # Ny ordre
                    new_order = Orders()
                    new_order.leilighet_id = apartment_id
                    new_order.status = [test]
                    new_order.leilighet_navn = apartment.apartment_id
                    new_order.standardprodukter = 1
                    db.session.add(new_order)
                    #db.session.flush
                    db.session.commit()
                    db.session.refresh(new_order)
                    
                    print("STANDARDPRODUKTER", standardproducts)    
                    
                    for room in standardproducts["rooms"]:
                        print(room)
                        room_id = (standardproducts["rooms"][room]["id"])
                        for category in standardproducts["rooms"][room]["categories"]:
                            print(category)
                            category_id = standardproducts["rooms"][room]["categories"][category]["id"]
                            for product in standardproducts["rooms"][room]["categories"][category]["products"]:
                                
                                # Ordredetaljer
                                new_order_details = Ordreoversikt()
                                new_order_details.ordre_id = new_order.id
                                new_order_details.produkt_id = product["product"].nrf
                                new_order_details.pris = product["price"]
                                new_order_details.antall = product["num"]
                                new_order_details.rom_id = room_id
                                new_order_details.kategori_id = category_id
                                db.session.add(new_order_details)
                                db.session.commit()
                                
                    return redirect(url_for("orders.order_list"))
                    #flash("order added")

        

        return render_template("orders.html", standard_apartment_order=standard_apartment_order, form=form, orders=apartment_order)
    return render_template("orders.html", standard_apartment_order=standard_apartment_order, form=form, orders=apartment_order)

@orders.route('/orders/<int:order_id>', methods=["GET", "POST"])
@login_required
def order_details(order_id):
    
    order = Orders.query.filter_by(id=order_id).first()
    
    ordreoversikt = Ordreoversikt.query.filter_by(ordre_id = order.id).all()

    ordrestatus = Status.query.join(order_statuses).filter(order_statuses.columns.orders_id == order.id).first()

    standardproducts = {
            "rooms": {},
            "totalPrice": 0,
            "status": ordrestatus.name
        }

    for item in ordreoversikt:
        room = Room.query.filter_by(id=item.rom_id).first()
        standardproducts["rooms"][room.name] = {
            "id": room.id,
            "categories": {}
        }
    
    for item in ordreoversikt:
        room = Room.query.filter_by(id=item.rom_id).first()
        categories = Category.query.filter_by(id=item.kategori_id).first()
        if item.id:
            standardproducts["rooms"][room.name]["categories"][categories.name] = {
                    "id": categories.id,
                    "products": {}
                }
    
    for item in ordreoversikt:
        room = Room.query.filter_by(id=item.rom_id).first()
        categories = Category.query.filter_by(id=item.kategori_id).first()
        product = Products.query.filter_by(nrf=item.produkt_id).first()
        if item.id:
            #standardproducts["rooms"][room.name]["categories"][categories.name]["products"].append(product)
            standardproducts["rooms"][room.name]["categories"][categories.name]["products"][product.nrf] = {
                #"nrf": product.nrf,
                "antall": item.antall,
                "navn": product.produktnavn,
                "price": item.pris * item.antall,
            }
            standardproducts["totalPrice"] += item.antall * item.pris
    
    

    
    print(standardproducts)

    return render_template("order_details.html", order=order, standardproducts=standardproducts)

@orders.route('/user_orders/', methods=["GET", "POST"])
@login_required
def order_list_admin():
    delete_form = DeleteOrder()
    all_orders = Orders.query.all()
    orders = Orders.query.group_by(Orders.leilighet_id).all()
    
    print(orders)

    if request.method == "POST":
        order_id = request.form["order_id"]
        print(order_id)
        delete_order_status = order_statuses.delete().where(order_statuses.columns.orders_id == order_id)
        delete_order_details = Ordreoversikt.__table__.delete().where(Ordreoversikt.ordre_id == order_id)
        delete_order = Orders.__table__.delete().where(Orders.id == order_id)
        db.session.execute(delete_order_status)
        db.session.execute(delete_order_details)
        db.session.execute(delete_order)
        db.session.commit()
        flash("Item deleted")
        return redirect(url_for("orders.order_list_admin"))        

    return render_template("orders_admin.html", orders=orders, all_orders=all_orders, delete_form=delete_form)


@orders.route('/orders/download/<string:id>', methods=['GET'])
def download_data(id):

    allProducts = {
                "rooms": {},
                "status": "",
                "totalPrice": 0,
            }

    # Alle ordrer
    orders = Orders.query.filter_by(leilighet_navn = id).all()

    produkt = []
    romnavn = []
    kategori = []
    nrf = []
    antall = []
    ordre = []
    dato = []
    total = []
    standardvare = []
    status = []
    
    for order in orders:
        print("ORDRE ID", order.id)
        ordrestatus = Status.query.join(order_statuses).filter(order_statuses.columns.orders_id == order.id).first()
        ordreoversikt = Ordreoversikt.query.filter_by(ordre_id = order.id).all()
        for ordredetaljer in ordreoversikt:
            print("ORDREOVERSIKT", ordredetaljer.id)
            rom = Room.query.filter_by(id=ordredetaljer.rom_id)
            for rom in rom:
                if not rom.file_upload:
                    print("ROM", rom)
                    romnavn.append(rom.name)
                    ordre.append(order.id)
                    allProducts["rooms"][rom.name] = {
                        "id":rom.id,
                        "categories": {}
                    }
                categories = Category.query.filter_by(id=ordredetaljer.kategori_id)
                for category in categories:
                    print("CATEGORIES", category.name)
                    kategori.append(category.name)
                    allProducts["rooms"][rom.name]["categories"][category.name] = {
                        "id":category.id,
                        "products": {}
                    }
                    product = Products.query.filter_by(nrf=ordredetaljer.produkt_id).first()
                    print("PRODUCT", product)
                    produkt.append(product.produktnavn)
                    nrf.append(product.nrf)
                    antall.append(ordredetaljer.antall)
                    dato.append(order.dato)
                    total.append(product.pris * ordredetaljer.antall)
                    standardvare.append(order.standardprodukter)
                    status.append(ordrestatus.name)
                    allProducts["rooms"][rom.name]["categories"][category.name]["products"][product.nrf] = {
                        #"nrf": product.nrf
                        "antall": ordredetaljer.antall,
                        "navn": product.produktnavn,
                        "bestillingsdato": order.dato,
                        "bestillingsid": order.id,
                        "standardvare": order.standardprodukter,
                        "totalpris": product.pris * ordredetaljer.antall,
                        "status": ordrestatus.name
                    }
                    allProducts["totalPrice"] += product.pris * ordredetaljer.antall

    print("ROMNAVN", romnavn)
    print(allProducts)
    
    excel.init_excel(app)
    extension_type = "xls"
    filename = "Ordresamling for " + id + "." + extension_type

    d = {
        'rom': romnavn,
        "kategori": kategori,
        "ordre-id": ordre,
        "produktnavn": produkt,
        "nrf": nrf,
        "antall": antall,
        "totalpris": total,
        "standardvare": standardvare,
        "status": status
        }
    
    return excel.make_response_from_dict(d, file_type=extension_type, file_name=filename)

###
@orders.route('/orders/download/<int:id>', methods=['GET'])
def download_order(id):
    
    produkt = []
    romnavn = []
    kategori = []
    nrf = []
    antall = []
    ordre = []
    dato = []
    total = []
    standardvare = []
    status = []

    allProducts = {
                "rooms": {},
                "status": "",
                "totalPrice": 0,
            }

    order = Orders.query.filter_by(id=id).first()

    ordreoversikt = Ordreoversikt.query.filter_by(ordre_id = order.id).all()

    standardproducts = {
            "rooms": {},
            "totalPrice": 0
        }

    for item in ordreoversikt:
        room = Room.query.filter_by(id=item.rom_id).first()
        romnavn.append(room.name)
        standardproducts["rooms"][room.name] = {
            "id": room.id,
            "categories": {}
        }
    
    for item in ordreoversikt:
        room = Room.query.filter_by(id=item.rom_id).first()
        categories = Category.query.filter_by(id=item.kategori_id).first()
        kategori.append(categories.name)
        if item.id:
            standardproducts["rooms"][room.name]["categories"][categories.name] = {
                    "id": categories.id,
                    "products": {}
                }
    
    for item in ordreoversikt:
        room = Room.query.filter_by(id=item.rom_id).first()
        categories = Category.query.filter_by(id=item.kategori_id).first()
        product = Products.query.filter_by(nrf=item.produkt_id).first()
        produkt.append(product.produktnavn)
        nrf.append(product.nrf)
        antall.append(item.antall)
        dato.append(order.dato)
        total.append(product.pris * item.antall)
        standardvare.append(order.standardprodukter)
        status.append(str(order.status[0]))
        ordre.append(order.id)
        if item.id:
            #standardproducts["rooms"][room.name]["categories"][categories.name]["products"].append(product)
            standardproducts["rooms"][room.name]["categories"][categories.name]["products"][product.nrf] = {
                #"nrf": product.nrf,
                "antall": item.antall,
                "navn": product.produktnavn,
                "price": item.pris * item.antall,
            }
            standardproducts["totalPrice"] += item.antall * item.pris
    
    excel.init_excel(app)
    extension_type = "xls"
    filename = "Ordre " + str(id) + "." + extension_type
    print(status)
    d = {
        'rom': romnavn,
        "kategori": kategori,
        "ordre-id": ordre,
        "produktnavn": produkt,
        "nrf": nrf,
        "antall": antall,
        "totalpris": total,
        "standardvare": standardvare,
        "status": status
        }

    return excel.make_response_from_dict(d, file_type=extension_type, file_name=filename)


@orders.route('/user_orders/<string:apartment_id>', methods=["GET", "POST"])
@login_required
def order_dashboard(apartment_id):
    
    allProducts = {
                "rooms": {},
                "status": "",
                "totalPrice": 0,
            }

    # Alle ordrer
    orders = Orders.query.filter_by(leilighet_navn = apartment_id).all()

    for order in orders:
        print("ORDRE ID", order.id)
        ordrestatus = Status.query.join(order_statuses).filter(order_statuses.columns.orders_id == order.id).first()
        print("ORDRESTATUS", ordrestatus)
        ordreoversikt = Ordreoversikt.query.filter_by(ordre_id = order.id).all()
        for ordredetaljer in ordreoversikt:
            print("ORDREOVERSIKT", ordredetaljer.id)
            print("ORDRE_KAT_ID", ordredetaljer.kategori_id)
            rom = Room.query.filter_by(id=ordredetaljer.rom_id)
            for rom in rom:
                if not rom.file_upload:
                    print("ROM", rom)
                    if not rom.name in allProducts["rooms"]:
                        allProducts["rooms"][rom.name] = {
                            "id":rom.id,
                            "categories": {}
                        }
                    
                categories = Category.query.filter_by(id=ordredetaljer.kategori_id)
                for category in categories:
                    print("KATEGORY", category.name)
                    allProducts["rooms"][rom.name]["categories"][category.name] = {
                        "id":category.id,
                        "products": {}
                    }
                    product = Products.query.filter_by(nrf=ordredetaljer.produkt_id).first()
                    print("PRODUCt", product.nrf)
                    allProducts["rooms"][rom.name]["categories"][category.name]["products"][product.nrf] = {
                        #"nrf": product.nrf
                        "antall": ordredetaljer.antall,
                        "navn": product.produktnavn,
                        "bestillingsdato": order.dato,
                        "bestillingsid": order.id,
                        "standardvare": order.standardprodukter,
                        "totalpris": product.pris * ordredetaljer.antall,
                        "status": ordrestatus.name
                    }
                    allProducts["totalPrice"] += product.pris * ordredetaljer.antall


    print(allProducts)
    
    user_folder = os.path.join(app.config['UPLOAD_PATH'], apartment_id)
    filenames= os.listdir(user_folder) # get all files' and folders' names in the current directory
    filestruct = {
    }
    for x in filenames:
        if os.path.isdir(os.path.join(os.path.abspath(user_folder), x)):
            filestruct[x] = []
            files = os.listdir(os.path.join(user_folder, x))
            for y in files:
                filestruct[x].append(y)


    print(filestruct)
    if os.path.isdir(user_folder):
        print(user_folder)
    return render_template("order_dashboard.html", allProducts=allProducts, filestruct=filestruct ,orders=orders, apartment_id=apartment_id)

@orders.route('/user_orders/<string:apartment_id>/<int:order_id>', methods=["GET", "POST"])
@login_required
def order_dashboard_order(apartment_id, order_id):
    form = ChangeStatus()
    order = Orders.query.filter_by(id=order_id).first()
    
    statuses = Status.query.all()
    print(order.status[0].id)
    for status in statuses:
        form.status.choices.insert(status.id,(status.name, status.name))
        form.status.default = order.status[0].name
        form.status.process([])

    ordreoversikt = Ordreoversikt.query.filter_by(ordre_id = order.id).all()

    standardproducts = {
            "rooms": {},
            "totalPrice": 0
        }

    for item in ordreoversikt:
        room = Room.query.filter_by(id=item.rom_id).first()
        standardproducts["rooms"][room.name] = {
            "id": room.id,
            "categories": {}
        }
    
    for item in ordreoversikt:
        room = Room.query.filter_by(id=item.rom_id).first()
        categories = Category.query.filter_by(id=item.kategori_id).first()
        if item.id:
            standardproducts["rooms"][room.name]["categories"][categories.name] = {
                    "id": categories.id,
                    "products": {}
                }
    
    for item in ordreoversikt:
        room = Room.query.filter_by(id=item.rom_id).first()
        categories = Category.query.filter_by(id=item.kategori_id).first()
        product = Products.query.filter_by(nrf=item.produkt_id).first()
        if item.id:
            #standardproducts["rooms"][room.name]["categories"][categories.name]["products"].append(product)
            standardproducts["rooms"][room.name]["categories"][categories.name]["products"][product.nrf] = {
                #"nrf": product.nrf,
                "antall": item.antall,
                "navn": product.produktnavn,
                "price": item.pris * item.antall,
            }
            standardproducts["totalPrice"] += item.antall * item.pris
    
    if request.method == "POST":
        flash("Status oppdatert")
        status_check = Status.query.filter_by(name=request.form["status"]).all()
        order.status = status_check
        db.session.commit()
        return redirect(request.url)

    
    print(standardproducts)

    return render_template("order_details.html", form=form, order=order, standardproducts=standardproducts)