from flask import Blueprint, render_template, url_for, request, flash, redirect
from flask_login import login_user, login_required, current_user, logout_user
from FT.models.apartments import Apartments
from FT.models.room import Room
from FT.models.collections import Collections, products_collections
from FT.models.category import Category
from FT.models.apartmenttype import Apartmenttype
from FT.models.products import Products
from FT.models.orders import Orders, Status
from FT.models.projects import Project
from FT.models.cart import Cart
from FT import db
from FT.forms.webforms import AddOrder
from FT.forms.webforms import DeleteFromCart
from FT.models.category import products_category
from FT.models.orders import Orders, Ordreoversikt
from sqlalchemy import delete


cart = Blueprint('cart', __name__, static_folder="static",
                 template_folder="templates")


# Landingsside for handlekurv
@cart.route('/cart', methods=["GET", "POST"])
@login_required
def cart_list():

    #Skjema
    form = AddOrder()
    deleteForm = DeleteFromCart()

    apartment_id = current_user.apartment_id
    
    standardproducts = {
            "rooms": {}
        }

    cart_items = Cart.query.filter_by(leilighet_id = current_user.apartment_id).all()

    for item in cart_items:
        room = Room.query.filter_by(id=item.rom).first()
        standardproducts["rooms"][room.name] = {
            "id": room.id,
            "categories": {}
        }
    
    for item in cart_items:
        room = Room.query.filter_by(id=item.rom).first()
        categories = Category.query.filter_by(id=item.kategori).first()
        if item.id:
            standardproducts["rooms"][room.name]["categories"][categories.name] = {
                    "id": categories.id,
                    "products": []
                }
    
    for item in cart_items:
        room = Room.query.filter_by(id=item.rom).first()
        categories = Category.query.filter_by(id=item.kategori).first()
        product = Products.query.filter_by(nrf=item.produkt_id).first()
        if item.id:
            standardproducts["rooms"][room.name]["categories"][categories.name]["products"].append(product)
    
    
    print(standardproducts)
    
    # Ordrestatus
    test = Status.query.filter_by(id = 1).all()

    if request.method == "POST":

            if form.submitOrder.data and form.validate():

                # Ny ordre
                new_order = Orders()
                new_order.leilighet_id = apartment_id
                new_order.status = test
                new_order.standardprodukter = 0
                db.session.add(new_order)
                #db.session.flush
                db.session.commit()
                db.session.refresh(new_order)

                

                for room in standardproducts["rooms"]:
                    print(room)
                    room_id = (standardproducts["rooms"][room]["id"])
                    for category in standardproducts["rooms"][room]["categories"]:
                        print(category)
                        category_id = standardproducts["rooms"][room]["categories"][category]["id"]
                        for product in standardproducts["rooms"][room]["categories"][category]["products"]:
                            print(product.produktnavn)
                            
                            # Ordredetaljer
                            new_order_details = Ordreoversikt()
                            new_order_details.ordre_id = new_order.id
                            new_order_details.produkt_id = product.nrf
                            new_order_details.antall = 1
                            new_order_details.rom_id = room_id
                            new_order_details.kategori_id = category_id
                            db.session.add(new_order_details)
                            db.session.commit()
                
                delete_q = Cart.__table__.delete().where(Cart.leilighet_id == apartment_id)
                db.session.execute(delete_q)
                db.session.commit()

                flash("order added")
                return redirect(url_for("cart.cart_list"))

            if deleteForm.deleteFromCart.data and form.validate():
                product = Products.query.filter_by(nrf=request.form["product_id"]).first()
                print(product.nrf)
                delete_q = Cart.__table__.delete().where(Cart.leilighet_id == apartment_id, Cart.produkt_id == product.nrf)
                db.session.execute(delete_q)
                db.session.commit()
                flash("Item deleted")
                return redirect(url_for("cart.cart_list"))

    
   
    return render_template("cart.html", standardproducts = standardproducts, form = form, cart_items = cart_items, deleteForm=deleteForm)
