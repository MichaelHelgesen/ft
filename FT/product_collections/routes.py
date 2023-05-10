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
from FT.models.room import Room
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
    
    room_form = webforms.AddRoomForm()
    removeForm = webforms.RemoveApartmentTypeForm()
    apartmentType = Apartmenttype.query.filter_by(slug=slug).first()
    projects = Project.query.all()
    apartmenttype_rooms = Room.query.filter_by(apartmenttype = apartmentType.id).all()
    print("APARTMENT ROOMS", apartmenttype_rooms)

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
        
        if room_form.submit_room.data and room_form.validate():
            new_room = Room()
            new_room.name = request.form["room_name"]
            new_room.slug = str_to_slug(request.form["room_name"])
            new_room.apartmenttype = apartmentType.id
            db.session.add(new_room)
            db.session.commit()
            flash("Room added")
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
                apartmentType.project_id = request.form["project"]
            db.session.commit()
            flash("Collection updated!")
            return redirect(url_for("product_col.collections"))
     
        else:
            flash("Error")
            return redirect(url_for("product_col.collections"))
        

    return render_template("collection.html", apartmenttype=apartmentType, form=form, projects=projects, room_form=room_form, apartmenttype_rooms=apartmenttype_rooms)

@product_col.route("/collections/<string:apartmenttype>/<string:slug>", methods=["GET", "POST"])
def collection_room(apartmenttype, slug):
    return render_template("room.html")

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