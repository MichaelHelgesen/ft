from flask import Blueprint, render_template, flash, redirect, url_for, request, jsonify
from FT.forms import webforms
from FT import db, app
import flask_excel as excel
import io
import pandas as pd
from functools import wraps
from FT.models.apartments import Apartments
from FT.models.projects import Projects
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
    form = webforms.AddApartmentForm()
    apartments = Apartments.query.all()
    projects = Projects.query.all()
    if request.method == "POST":
        if form.validate_on_submit():
            apartment_id = form.apartment_id.data.upper()  
            apartment = Apartments.query.filter_by(apartment_id = apartment_id).first()
            if apartment is None:
                new_apartment = Apartments()
                new_apartment.id = apartment_id
                new_apartment.slug = str_to_slug(apartment_id)
                db.session.add(new_apartment)
                db.session.commit()
                form.apartment_id.data = ""
                flash("project added")
                return redirect(url_for("apartments.apartments_list"))
            else:
                flash("project name already exists")
                return redirect(url_for("apartments.apartments_list"))
        else:
            flash("Something went wrong")
            return render_template("apartments.html", form=form)
    return render_template("apartments.html", form=form, apartments=apartments, projects=projects)


@apartments.route('/apartments/<string:slug>', methods=["GET", "POST"])
def apratment_edit(slug):
    project = Projects.query.filter_by(slug=slug).first()
    name = project.name
    return render_template("apartments_edit.html", name=name.title())

