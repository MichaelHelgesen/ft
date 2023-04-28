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
from FT.models.projects import Project
from FT.models.products import Products
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
    
    collections = Collections.query.all()
    projects = Project.query.all()

    if projects:
        form = webforms.AddCollection()
        form.project.choices = [(project.id, project.name.title()) for project in projects]
        form.project.choices.insert(0, ("", "Velg prosjekt"))
    else:
        form = webforms.AddCollectionNoProjectForm()


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

    return render_template("collections.html", form=form, collections=collections, projects=projects)

@product_col.route("/collections/<string:slug>", methods=["GET", "POST"])
def collection(slug):
    
    addForm = webforms.AddToCollection()
    collection = Collections.query.filter_by(slug=slug).first()
    #product_collection = products_collections.query.all()
    products = Products.query.all()
    projects = Project.query.all()
    #selectedProducts  = Products.query.filter_by()

    if projects:
        form = webforms.AddCollection()
        current_collection_project = Project.query.filter_by(id = collection.project_id).first()
        #updateForm = webforms.UpdateCollectionForm()
        form.project.choices = [(project.id, project.name.title()) for project in projects]
        if current_collection_project:
            form.project.choices.insert(0,("", "Ingen prosjekt valgt"))
            form.project.default = current_collection_project.id
            form.project.process([])
        else:
            form.project.choices.insert(0,("", "Ingen prosjekt valgt"))
    else:
        form = form = webforms.AddCollectionNoProjectForm()
  
    form.collection_name.data = collection.name
    
    if request.method == "POST":

        if addForm.submit2.data and addForm.validate():
            print(addForm.data)
            flash("Added to collection!")
            print(request.form["product_id"])
            print(Products.query.filter_by(nrf=request.form["product_id"]).first())
            #collection.product = Products.query.filter_by(nrf=request.form["product_id"]).first()
            collection.product.append(Products.query.filter_by(nrf=request.form["product_id"]).first())
            db.session.commit()
            return redirect(request.url)

        if form.submit.data and form.validate():
            print("test2")
            collection.name = request.form["collection_name"].upper()
            collection.slug = str_to_slug(request.form["collection_name"])
            if projects:
                collection.project_id = request.form["project"]
            db.session.commit()
            flash("Collection updated!")
            return redirect(url_for("product_col.collections"))
                
        else:
            flash("Error")
            return redirect(url_for("product_col.collections"))
        

    return render_template("collection.html", collection=collection, form=form, projects=projects, products=products, addForm=addForm)

@product_col.route("/collections/delete/<string:name>", methods=["GET", "POST"])
def delete_col(name):
    col_to_delete = Collections.query.filter_by(name=name).first()
    try:
        db.session.delete(col_to_delete)
        db.session.commit()
        flash("Collection deleted")
        return redirect(url_for("product_col.collections"))
    except:
        flash("There was a problem")
        return redirect(url_for("product_col.collections"))