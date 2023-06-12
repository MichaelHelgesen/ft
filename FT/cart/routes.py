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
from FT import db, app
from FT.forms.webforms import AddOrder
from FT.forms.webforms import DeleteFromCart
from FT.models.category import products_category
from FT.models.orders import Orders, Ordreoversikt
from sqlalchemy import delete
import smtplib
from tabulate import tabulate
from flask_redmail import RedMail
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText


cart = Blueprint('cart', __name__, static_folder="static",
                 template_folder="templates")


# Landingsside for handlekurv
@cart.route('/cart', methods=["GET", "POST"])
@login_required
def cart_list():

    # Skjema
    form = AddOrder()
    deleteForm = DeleteFromCart()

    apartment_id = current_user.apartment_id
    print("APARTMENT ID", apartment_id)
    apartment = Apartments.query.filter_by(id = apartment_id).first()
    print("APARTMENT", apartment)
    standardproducts = {
        "rooms": {},
        "totalPrice": 0
    }

    cart_items = Cart.query.filter_by(
        leilighet_id=current_user.apartment_id).all()

    for item in cart_items:
        room = Room.query.filter_by(id=item.rom).first()
        standardproducts["rooms"][room.name] = {
            "id": room.id,
            "categories": {},
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
            standardproducts["rooms"][room.name]["categories"][categories.name]["products"].append({
                "product": product,
                "price": product.pris,
                "num": item.antall,
                "unit": product.enhet
            })
            standardproducts["totalPrice"] += item.antall * product.pris

    print(standardproducts)

    # Ordrestatus
    test = Status.query.filter_by(id=1).all()

    if request.method == "POST":

        if form.submitOrder.data and form.validate():

            # Ny ordre
            new_order = Orders()
            new_order.leilighet_id = apartment_id
            new_order.status = test
            new_order.standardprodukter = 0
            new_order.leilighet_navn = apartment.apartment_id
            db.session.add(new_order)
            # db.session.flush
            db.session.commit()
            db.session.refresh(new_order)

            for room in standardproducts["rooms"]:
                print(room)
                room_id = (standardproducts["rooms"][room]["id"])
                for category in standardproducts["rooms"][room]["categories"]:
                    print(category)
                    category_id = standardproducts["rooms"][room]["categories"][category]["id"]
                    for product in standardproducts["rooms"][room]["categories"][category]["products"]:
                        print(product["product"])

                        # Ordredetaljer
                        new_order_details = Ordreoversikt()
                        new_order_details.ordre_id = new_order.id
                        new_order_details.pris = product["price"]
                        new_order_details.produkt_id = product["product"].nrf
                        new_order_details.antall = product["num"]
                        new_order_details.rom_id = room_id
                        new_order_details.kategori_id = category_id
                        db.session.add(new_order_details)
                        db.session.commit()

            delete_q = Cart.__table__.delete().where(Cart.leilighet_id == apartment_id)
            db.session.execute(delete_q)
            db.session.commit()

            def getHTML(dict):
                html = ""
                for room in dict:
                    print(room)
                    room_id = (dict[room]["id"])
                    for category in dict[room]["categories"]:
                        category_id = dict[room]["categories"][category]["id"]
                        for product in dict[room]["categories"][category]["products"]:
                            html += "<tr>\
                                        <td>" + product["product"].produktnavn + " " + product["product"].farge + "</td>\
                                        <td>" + str(product["product"].nrf) + "</td>\
                                        <td>" + room + "</td>\
                                        <td>" + category + "</td>\
                                        <td>" + str(product["num"]) + "</td>\
                                        <td>" + str(product["price"]) + "</td>\
                                        <td>" + str(product["price"] * product["num"]) + "</td>\
                                    </tr>"
                return html
                            

            # SENDE MAIL
            # me == my email address
            # you == recipient's email address
            me = "michaelhelgesen02@gmail.com"
            you = "michael@leonberg.no"

            # Create message container - the correct MIME type is multipart/alternative.
            msg = MIMEMultipart('alternative')
            msg['Subject'] = "Link"
            msg['From'] = me
            msg['To'] = you

            table = [['one', 'two', 'three'], [
                'four', 'five', 'six'], ['seven', 'eight', 'nine']]

            # Create the body of the message (a plain-text and an HTML version).
            text = "Hi!\nHow are you?\nHere is the link you wanted:\nhttp://www.python.org"
            html = """\
                <p>Ny bestilling av tilvalg til leilighet """ + str(apartment_id) + """</p>
                <p>Eier: """ + current_user.name + """</p>
                <p>E-post: """ + current_user.email + """</p>
                <table width="100%" cellspacing="0" cellpadding="0" style="border:solid 1px #cccccc">
                    <tbody>
                        <tr>
                            <th style="color:#000000;background-color:#cccccc;text-align:left;padding:5px">Produkt</th>
                            <th style="color:#000000;background-color:#cccccc;text-align:left;padding:5px">Artikkelnr.</th>
                            <th style="color:#000000;background-color:#cccccc;text-align:left;padding:5px">Rom</th>
                            <th style="color:#000000;background-color:#cccccc;text-align:left;padding:5px">Kategori</th>
                            <th style="color:#000000;background-color:#cccccc;text-align:left;padding:5px">Antall</th>
                            <th style="color:#000000;background-color:#cccccc;text-align:left;padding:5px">Enhetspris</th>
                            <th style="color:#000000;background-color:#cccccc;text-align:left;padding:5px">Totalpris</th>
                        </tr> 
                        """ + getHTML(standardproducts["rooms"]) + """
                    </tbody>
                </table>
                <p>
                    Totalpris:""" + str(standardproducts["totalPrice"]) + """
                </p>"""
                
                

            # Record the MIME types of both parts - text/plain and text/html.
            part1 = MIMEText(text, 'plain')
            part2 = MIMEText(html, 'html')

            # Attach parts into message container.
            # According to RFC 2046, the last part of a multipart message, in this case
            # the HTML message, is best and preferred.
            msg.attach(part1)
            msg.attach(part2)

            """ message = "Ny bestilling av tilvalg til leilighet " + str(apartment_id)
                message += "\n Eier: " + current_user.name
                message += "\n Epost: " + current_user.email
                message += "\n Produkter: \n"

                table = [['one','two','three'],['four','five','six'],['seven','eight','nine']]

                #print(tabulate(table, tablefmt='html'))

                message += tabulate(table, tablefmt='html') """

            server = smtplib.SMTP("smtp.gmail.com", 587)
            server.starttls()
            server.login(me, "")
            server.sendmail(me, you, msg.as_string())
            server.quit()

            flash("order added")
            return redirect(url_for("cart.cart_list"))

        if deleteForm.deleteFromCart.data and form.validate():
            product = Products.query.filter_by(
                nrf=request.form["product_id"]).first()
            print(product.nrf)
            delete_q = Cart.__table__.delete().where(
                Cart.leilighet_id == apartment_id, Cart.produkt_id == product.nrf)
            db.session.execute(delete_q)
            db.session.commit()
            flash("Item deleted")
            return redirect(url_for("cart.cart_list"))

    return render_template("cart.html", standardproducts=standardproducts, form=form, cart_items=cart_items, deleteForm=deleteForm)
