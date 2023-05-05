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
from FT.models.collections import Collections, products_collections
from FT.models.apartmenttype import Apartmenttype
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
    
    apartmenttypes = Apartmenttype.query.all()
    projects = Project.query.all()
    print(projects)
    
    if projects:
        form = webforms.AddApartmentTypeForm()
        form.project.choices = [(project.id, project.name.title()) for project in projects]
        form.project.choices.insert(0, ("", "Velg prosjekt"))
    else:
        form = webforms.AddApartmentTypeNoProjectForm()

    print(form)

    if request.method == "POST":
        if form.validate_on_submit():
            apartmenttype_id = form.apartmenttype_name.data.upper()  
            apartmenttype = Apartmenttype.query.filter_by(name = apartmenttype_id).first()
            if apartmenttype is None:
                new_apartmenttype = Apartmenttype()
                new_apartmenttype.project_id = request.form["project"]
                new_apartmenttype.name = apartmenttype_id
                new_apartmenttype.slug = str_to_slug(request.form["apartmenttype_name"])
                db.session.add(new_apartmenttype)
                db.session.commit()
                form.apartmenttype_name.data = ""
                flash("apartmenttype added")
                return redirect(url_for("product_col.collections", form=form, apartmenttypes=apartmenttypes, projects=projects))
            else:
                flash("Collection name already exists")
                return redirect(url_for("product_col.collections", form=form, apartmenttypes=apartmenttypes, projects=projects))
        else:
            flash("Something wrong")
            return redirect(url_for("product_col.collections", form=form, apartmenttypes=apartmenttypes, projects=projects))   

    return render_template("collections.html", form=form, apartmenttypes=apartmenttypes, projects=projects)




@product_col.route("/collections/<string:slug>", methods=["GET", "POST"])
def collection(slug):
    
    addForm = webforms.UpdateApartmentTypeForm()
    removeForm = webforms.RemoveApartmentTypeForm()
    apartmentType = Apartmenttype.query.filter_by(slug=slug).first()
    apartmentTypes = Apartmenttype.query.all()
    #product_collection = db.Table.query(products_collections).query.all()
    products = Products.query.all()
    projects = Project.query.all()
    #chosenProducts = db.session.query(Products).join(Apartmenttype.product).filter(apartmentType.name == apartmentType.name).all()
    #productsAvaliable = db.session.query(Products).outerjoin(products_collections, Products.nrf == products_collections.columns.products_id).filter(products_collections.columns.products_id == None).all()

    #selectedProducts  = Products.query.filter_by()
    products_not_in_collection = Products.query.filter_by(nrf = "5524").all()
    #test2 = Collections.query.filter_by(name = "TEST2").first()
    #print(test2)
    #test = Products.query.join(test2.product).all()
    #test3 = db.session.query(Collections, products_collections).filter(Collections = "5524").all()
    #print("PRODUCTS IN COLLETION: ", test4)
    #test6 = db.session.query(Products).join(Collections.product).filter(Collections.name == collection.name)

    #test5 = db.session.query(Products).join(products_collections).filter(products_collections.columns.products_id.in_(test6)).all()
    #test7 = db.session.query(Products, products_collections).filter(Products.nrf != products_collections.columns.products_id).all()
    #test8 = db.session.query(Products).join(products_collections).filter(Products.nrf.in_([products_collections.columns.products_id])).all()
    #print("PRODUCTS NOT IN COLLETION: ", test7)
    #query = query.filter(table_a.id.not_in(subquery))

    if projects:
        form = webforms.AddApartmentTypeForm()
        current_apartmenttype_project = Project.query.filter_by(id = apartmentType.project_id).first()
        #updateForm = webforms.UpdateCollectionForm()
        form.project.choices = [(project.id, project.name.title()) for project in projects]
        if current_apartmenttype_project:
            form.project.choices.insert(0,("", "Ingen prosjekt valgt"))
            form.project.default = current_apartmenttype_project.id
            form.project.process([])
        else:
            form.project.choices.insert(0,("", "Ingen prosjekt valgt"))
    else:
        form = form = webforms.AddApartmentTypeNoProjectForm()
  
    form.apartmenttype_name.data = apartmentType.name
    
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

        if removeForm.submit3.data and removeForm.validate():
            flash("Removed from collection!")
            #print(request.form["product_id"])
            #print(Products.query.filter_by(nrf=request.form["product_id"]).first())
            #collection.product = Products.query.filter_by(nrf=request.form["product_id"]).first()
            collection.product.remove(Products.query.filter_by(nrf=request.form["product_id"]).first())
            db.session.commit()
            return redirect(request.url)

        if form.submit.data and form.validate():
            apartmentType.name = request.form["apartmenttype_name"].upper()
            apartmentType.slug = str_to_slug(request.form["apartmenttype_name"])
            if projects:
                collection.project_id = request.form["project"]
            db.session.commit()
            flash("Collection updated!")
            return redirect(url_for("product_col.collections"))
     
        else:
            flash("Error")
            return redirect(url_for("product_col.collections"))
        

    return render_template("collection.html", apartmenttype=apartmentType, form=form, projects=projects)

@product_col.route("/collections/delete/<string:name>", methods=["GET", "POST"])
def delete_col(name):
    col_to_delete = Apartmenttype.query.filter_by(name=name).first()
    try:
        db.session.delete(col_to_delete)
        db.session.commit()
        flash("Collection deleted")
        return redirect(url_for("product_col.collections"))
    except:
        flash("There was a problem")
        return redirect(url_for("product_col.collections"))