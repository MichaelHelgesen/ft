from flask import Blueprint, render_template, flash, redirect, url_for, request, jsonify
from FT.forms import webforms
from FT import db, app
import flask_excel as excel
import io
import pandas as pd
from functools import wraps
from FT.models.apartments import Apartments
from FT.models.projects import Project
from FT.models.collections import Collections
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, login_required, current_user, logout_user
import csv
import re

apartments = Blueprint('apartments', __name__, static_folder="static",
                  template_folder="templates")

def str_to_slug(string, delimeter = "-"):
    slug = re.sub(r"[^\w\d\s]", "", string.strip().lower())
    slug = re.sub(" +", " ", slug)
    slug = slug.replace(" ", delimeter)
    return slug

@apartments.route('/apartments', methods=["GET", "POST"])
def apartments_list():
    apartments = Apartments.query.all()
    projects = Project.query.all()

    if projects:
        form = webforms.AddApartmentForm()
        form.project.choices = [(project.id, project.name.title()) for project in projects]
        form.project.choices.insert(0, ("", "Velg prosjekt"))
    else:
        form = webforms.AddApartmentNoProjectForm()
    
    

    #form.project.choices = [(project.id, project.name.title()) for project in projects]
    if request.method == "POST":
        if form.validate_on_submit():
            apartment_id = form.apartment_id.data.upper()  
            apartment = Apartments.query.filter_by(apartment_id = apartment_id).first()
            if apartment is None:
                new_apartment = Apartments()
                new_apartment.apartment_id = apartment_id
                new_apartment.slug = str_to_slug(apartment_id)
                if projects:
                    new_apartment.project_id = form.project.data
                db.session.add(new_apartment)
                db.session.commit()
                form.apartment_id.data = ""
                flash("apartment added")
                return redirect(url_for("apartments.apartments_list"))
            else:
                flash("apartment name already exists")
                return redirect(url_for("apartments.apartments_list"))
        else:
            flash("Something went wrong")
            return render_template("apartments.html", form=form)
    if projects:
        return render_template("apartments.html", form=form, apartments=apartments, projects=projects)
    return render_template("apartments.html", form=form, apartments=apartments)



@apartments.route('/apartments/<string:slug>', methods=["GET", "POST"])
def apartment_edit(slug):
    apartment = Apartments.query.filter_by(slug=slug).first()
    apartment_id = apartment.apartment_id.upper()
    id = apartment.id
    projects = Project.query.all()
    current_apartment_project = Project.query.filter_by(id = apartment.project_id).first()
    form = webforms.UpdateApartmentForm()
    
    if projects:
        form.project.choices = [(project.id, project.name.title()) for project in projects]
        form.project.choices.insert(0,("", "Ingen prosjekt valgt"))
        if current_apartment_project:
            form.project.default = current_apartment_project.id
            form.project.process([])
    else:
        form = webforms.AddApartmentNoProjectForm()
        #form.project.choices.insert(0,("", "Ingen prosjekt valgt"))

    form.apartment_id.data = id
    
    if request.method == "POST":
        if form.validate_on_submit():
                apartment.apartment_id = request.form["apartment_id"].upper()
                apartment.slug = str_to_slug(request.form["apartment_id"])
                if projects:
                    apartment.project_id = request.form["project"]
                db.session.commit()
                flash("User updated!")
                return redirect(url_for("apartments.apartments_list"))
                
        else:
            flash("Error")
            return redirect(url_for("apartments.apartments_list"))
    
    return render_template("apartment_edit.html", apartment_id=apartment_id, id=id, form=form, slug=slug, projects=projects)

@apartments.route("/apartments/delete/<int:id>")
@login_required
def delete_apartment(id):
    apartment_to_delete = Apartments.query.get_or_404(id)
    try:
        db.session.delete(apartment_to_delete)
        db.session.commit()
        flash("Apartment deleted")
        return redirect(url_for("apartments.apartments_list"))
    except:
        flash("There was a problem")
        return redirect(url_for("apartments.apartments_list"))