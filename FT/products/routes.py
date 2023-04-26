from flask import Blueprint, render_template, flash, redirect, url_for, request
from FT.forms import webforms
import sqlalchemy
from FT import db, app
import flask_excel as excel
import pandas as pd
import sqlite3
import os
import urllib
from functools import wraps
from FT.models.products import Products
from FT.models.apartments import Apartments
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, login_required, current_user, logout_user


products = Blueprint('products', __name__, static_folder="static", static_url_path='/', template_folder="templates")

@products.route("/products", methods=["GET", "POST"])
def product_list():
    products = Products.query.all()
    importform = webforms.ImportForm()
    addform = webforms.AddProductForm()
    
    if request.method == "POST":
        if importform.submit.data and importform.validate():
            print("importskjema")
            #df = pd.read_csv(request.files.get('file'))
            df = pd.read_excel(request.files.get('file'))
            
            for index in df.index:
                check_product = Products.query.filter_by(nrf = df["NRF"][index]).first()
                if check_product is None:
                    product = Products()
                    product.slug = urllib.parse.quote(str(df["NRF"][index]) + "-" + df["Produktnavn"][index].replace('.','').replace(' ','-'))
                    product.nrf = str(df["NRF"][index])
                    product.leverandor = df["Leverandør"][index]
                    product.hovedkategori = df["Hovedkategori"][index]
                    product.underkategori = df["Underkategori"][index]
                    product.kategori = df["Kategori"][index]
                    product.produktnavn = df["Produktnavn"][index]
                    product.beskrivelse = df["Beskrivelse"][index]
                    product.mal = df["Mål"][index]
                    product.farge = df["Farge"][index]
                    product.enhet = df["Enhet"][index]
                    db.session.add(product)
                    db.session.commit()
                    products = Products.query.all()
            flash("imported")
            return render_template('product_list.html', products=products, importform=importform)
        
        if addform.submit.data and addform.validate():
            print("legg til produkt-skjema")
            print(Products.query.filter_by(nrf = request.form["nrf"]).first())
            product_id = request.form["nrf"]
            check_if_product_exist = Products.query.filter_by(nrf = request.form["nrf"]).first()
            print(check_if_product_exist)
            if check_if_product_exist is None:
                product = Products()
                product.slug = urllib.parse.quote(str(request.form["nrf"]) + "-" + request.form["produktnavn"].replace('.','').replace(' ','-'))
                product.nrf = str(request.form["nrf"])
                product.leverandor = request.form["leverandor"]
                product.hovedkategori = request.form["hovedkategori"]
                product.underkategori = request.form["underkategori"]
                product.kategori = request.form["kategori"]
                product.produktnavn = request.form["produktnavn"]
                product.beskrivelse = request.form["beskrivelse"]
                product.mal = request.form["mal"]
                product.farge = request.form["farge"]
                product.enhet = request.form["enhet"]
                db.session.add(product)
                db.session.commit()
                products = Products.query.all()
                print("test")
                flash("product added")
                return render_template('product_list.html', products=products, importform=importform, addform=addform)
            else:
                flash("product already exists")
                return render_template('product_list.html', products=products, importform=importform, addform=addform)
    
    return render_template("product_list.html", importform=importform, products=products, addform=addform)

    """ con = sqlite3.connect("instance/ft.db")
    con.row_factory = sqlite3.Row
    

    cur = con.cursor()
    cur.execute("select * from products")
   
    rows = cur.fetchall()
    
  
    if request.method == "POST":
        if form.validate_on_submit():
            if not sqlalchemy.inspect(db.engine).has_table("products"):
                df = pd.read_excel(request.files.get('file'))
                df.head()
                df.to_sql('products', con=db.engine)
                flash("Products imported")
                return redirect(url_for("products.product_list"))
            else:
                flash("Table PRODUCTS already exists")
                return redirect(url_for("products.product_list"))
        else: 
            flash("Error")
            return redirect(url_for("products.product_list")) """
    
    #return render_template("product_list.html", form=form, rows=rows)

@products.route('/products/download', methods=['GET'])
def download_data():
    #products = products.query.all()
    
    con = sqlite3.connect("instance/ft.db")
    
    con.row_factory = sqlite3.Row #Gir oss navn på kolonner 
    cur = con.cursor()
    cur.execute("select * from products")
    products = cur.fetchall()

    product_nrf = []
    product_names = []

    for product in products:
        print(dict(product)["NRF"])
        product_nrf.append(dict(product)["NRF"])
        product_names.append(dict(product)["Produktnavn"])

    print(product_nrf)

    excel.init_excel(app)
    extension_type = "xls"
    filename = "test123" + "." + extension_type
    d = {'nrf': product_nrf, "Produktnavn": product_names}

    return excel.make_response_from_dict(d, file_type=extension_type, file_name=filename)

@products.route('/products/<string:slug>', methods=["GET", "POST"])
def product_edit(slug):
    product = Products.query.filter_by(slug=slug).first()
    product_id = product.nrf
    image_file = url_for('products.static', filename=str(product_id) + ".jpg")
    return render_template("product.html", product_id=product_id, id=id, slug=slug, product=product, image_file=image_file)

@products.route("/products/delete/<string:id>")
@login_required
def delete_product(id):
    product_to_delete = Products.query.filter_by(nrf=id).first()
    try:
        db.session.delete(product_to_delete)
        db.session.commit()
        flash("Product deleted")
        return redirect(url_for("products.product_list"))
    except:
        flash("There was a problem")
        return redirect(url_for("products.product_list"))

