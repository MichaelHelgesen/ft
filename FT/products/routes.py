from flask import Blueprint, render_template, flash, redirect, url_for, request
from FT.forms import webforms
import sqlalchemy
from FT import db, app
import flask_excel as excel
import pandas as pd
import sqlite3
from functools import wraps
from FT.models.products import Products
from FT.models.apartments import Apartments
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, login_required, current_user, logout_user


products = Blueprint('products', __name__, static_folder="static",
                  template_folder="templates")

@products.route("/products", methods=["GET", "POST"])
def product_list():
    form = webforms.ImportForm()
    
    con = sqlite3.connect("instance/ft.db")
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
            return redirect(url_for("products.product_list"))
    
    return render_template("product_list.html", form=form, rows=rows)

""" @products.route('/products/download', methods=['GET'])
def download_data():
    users = Users.query.all()
    user_id = []
    user_names = []
    user_emails = []
    user_username = []
    for users in users:
        user_id.append(users.id)
        user_names.append(users.name)
        user_emails.append(users.email)
        user_username.append(users.username)
        print(users.role)
    excel.init_excel(app)
    extension_type = "xls"
    filename = "test123" + "." + extension_type
    d = {'id': user_id, "name": user_names, "email": user_emails, "username": user_username}
    return excel.make_response_from_dict(d, file_type=extension_type, file_name=filename) """