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
from FT.models.collections import Collections
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, login_required, current_user, logout_user
import re


product_col = Blueprint('product_col', __name__, static_folder="static", static_url_path='/', template_folder="templates")

def str_to_slug(string, delimeter = "-"):
    slug = re.sub(r"[^\w\d\s]", "", string.strip().lower())
    slug = re.sub(" +", " ", slug)
    slug = slug.replace(" ", delimeter)
    return slug

@product_col.route("/collections", methods=["GET", "POST"])
def collections():
    form = webforms.AddCollection()
    collections = Collections.query.all()

    if request.method == "POST":
        if form.validate_on_submit():
            collection_id = form.collection_name.data.upper()  
            collection = Collections.query.filter_by(name = collection_id).first()
            if collection is None:
                new_collection = Collections()
                new_collection.name = collection_id
                new_collection.slug = str_to_slug(request.form["collection_name"])
                db.session.add(new_collection)
                db.session.commit()
                form.collection_name.data = ""
                flash("collection added")
                return redirect(url_for("product_col.collections", form=form, collections=collections))
            else:
                flash("Collection name already exists")
                return redirect(url_for("product_col.collections", form=form, collections=collections))

    return render_template("collections.html", form=form, collections=collections)

@product_col.route("/collections/<string:slug>", methods=["GET", "POST"])
def collection(slug):
    return render_template("collection.html")