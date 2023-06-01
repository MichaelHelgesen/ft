from flask import Blueprint, render_template, flash, redirect, url_for, request, jsonify
from FT.forms import webforms
from FT import db, app
import flask_excel as excel
import io
import numpy as np
import pandas as pd
from functools import wraps
from FT.models.apartments import Apartments, Apartmentdata
from FT.models.projects import Project
from FT.models.apartmenttype import Apartmenttype
from FT.models.apartments import apartments_apartmenttypes, Apartmentdata
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, login_required, current_user, logout_user
import csv
import re

apartments = Blueprint('apartments', __name__, static_folder="static",
                  template_folder="templates")

# URL-vennlig path
def str_to_slug(string, delimeter = "-"):
    slug = re.sub(r"[^\w\d\s]", "", string.strip().lower())
    slug = re.sub(" +", " ", slug)
    slug = slug.replace(" ", delimeter)
    return slug

# Landingsside for alle leiligheter
@apartments.route('/apartments', methods=["GET", "POST"])
def apartments_list():
    
    import_form = webforms.ImportForm()

    # Alle leiligheter
    apartments = Apartments.query.all()
    
    # Alle prosjekter
    projects = Project.query.all()

    # Vis nedtrekksmeny for prosjekter hvis prosjekter eksisterer
    if projects:
        form = webforms.AddApartmentForm()
        form.project.choices = [(project.id, project.name.title()) for project in projects]
        form.project.choices.insert(0, ("", "Velg prosjekt"))
    else:
        form = webforms.AddApartmentNoProjectForm()

    #form.project.choices = [(project.id, project.name.title()) for project in projects]
    
    # Hvis nytt prosjekt registreres via skjema
    if request.method == "POST":
        if form.submit_apartment.data and form.validate():
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
        
        if import_form.submit.data and import_form.validate():
            flash("import")
            print(request.files.get('file'))
            df = pd.read_excel(request.files.get('file'))
            #test = list(df.columns.values)
            #print(test)

            for x in df.columns.values:
                if x != "Rom":
                    print(x)
                    import_apartment = Apartments()
                    import_apartment.apartment_id = x
                    import_apartment.slug = str_to_slug(x)
                    db.session.add(import_apartment)
                    db.session.commit()
                    db.session.refresh(import_apartment)
                    for index in df.index:
                        import_apartment_data = Apartmentdata()
                        import_apartment_data.datatype = df["Rom"][index]
                        import_apartment_data.verdi = int(df[x][index])
                        import_apartment_data.apartment_id = import_apartment.id
                        db.session.add(import_apartment_data)
                        db.session.commit()
                        #id = db.Column(db.Integer, primary_key=True)
                        #datatype = db.Column(db.String(200), nullable=False)
                        #verdi = db.Column(db.Integer)
                        #apartment_id = db.Column(db.I
                        print(df["Rom"][index])
                        print(int(df[x][index]))
            return redirect(url_for("apartments.apartments_list"))  
          
        
        else:
            flash("Something went wrong")
            return render_template("apartments.html", form=form, import_form=import_form)
        
    if projects:
        return render_template("apartments.html", import_form=import_form, form=form, apartments=apartments, projects=projects)
    return render_template("apartments.html", form=form, apartments=apartments, import_form=import_form)


# Landingsside leilighet
@apartments.route('/apartments/<string:slug>', methods=["GET", "POST"])
def apartment_edit(slug):
    # Finn den aktuelle leiligheten
    apartment = Apartments.query.filter_by(slug=slug).first()
    apartment_id = apartment.apartment_id.upper()
    id = apartment.id

    # Hent leilighetsdata
    apartment_data = Apartmentdata.query.filter_by(apartment_id = id).all()
    print(apartment_data)

    # Hent alle prosjekter
    projects = Project.query.all()
    # Hent gjeldende leilighets tilknyttede prosjekt, hvis noen
    current_apartment_project = Project.query.filter_by(id = apartment.project_id).first()

    # Hent alle leilighetstyper 
    apartmenttypes = None
    # Hent gjeldende leilighets tilknyttede leilighetstype, hvis noen
    current_apartmenttype = Apartmenttype.query.filter_by(id = apartment.apartmenttype_id).first()
    
    if current_apartmenttype:
        print("Satt leilighetstype?", current_apartmenttype.id)
    else:
        print("INGEN LEILIGHETSTYPE SATT")
    if current_apartment_project:
        print("Satt prosjekt" , current_apartment_project)
    else:
        print("INGEN PROSJEKT SATT")
    
    form = webforms.UpdateApartmentNoProjectForm()

    # Oppdateringsskjema
    #if projects:
        #form = webforms.UpdateApartmentForm()
    #else:
        #form = webforms.UpdateApartmentNoProjectForm
    


    # Hent tilknyttede leilighetstyper hvis eksisterer, 
    # og prosjekt er valgt
    #apartmenttypes = Apartmenttype.query.filter_by(project_id = current_apartment_project.id).all()
    if current_apartment_project:
        apartmenttypes = Apartmenttype.query.filter_by(project_id = current_apartment_project.id).all()

    # Vis nedtrekksmeny for prosjekter hvis prosjekter eksisterer, 
    # og vis tilknyttet prosjekt hvis satt
    print("PROSJEKTER", projects)

    if projects:
        form = webforms.UpdateApartmentNoApartmenttypeForm()
        if current_apartment_project:
            form = webforms.UpdateApartmentForm()
        if not apartmenttypes:
            form = webforms.UpdateApartmentNoApartmenttypeForm()
    else:
        form = webforms.AddApartmentNoProjectForm()

    print(form)
    print("Leilighetstyper", apartmenttypes)
    print("Current leilighetstype", current_apartmenttype)

    if projects:
        #form = webforms.UpdateApartmentNoApartmenttypeForm()
        form.project.choices = [(project.id, project.name.title()) for project in projects]
        form.project.choices.insert(0,("", "Ingen prosjekt valgt"))
        if current_apartment_project:
            #form = webforms.UpdateApartmentForm()
            # Sett valgt prosjekt som default i nedtrekksmenyen
            form.project.default = current_apartment_project.id
            form.project.process([])
            #form.apartmenttype.choices = [(apartmenttype.id, apartmenttype.name.title()) for apartmenttype in apartmenttypes]
            # Vis nedtrekksmeny for leilighetstyper hvis leilighetstyper eksisterer, 
            # og vis tilknyttet leilighetstype hvis satt 
            if projects and current_apartment_project and apartmenttypes:
                form.apartmenttype.choices = [(apartmenttype.id, apartmenttype.name.title()) for apartmenttype in apartmenttypes]
                form.apartmenttype.choices.insert(0,("", "Ingen leilighetstype valgt"))
                if current_apartmenttype:
                    # Sett valgt prosjekt som default i nedtrekksmenyen
                    form.apartmenttype.default = current_apartmenttype.id
                    form.apartmenttype.process([])
            #else:
                #form = webforms.UpdateApartmentNoApartmenttypeForm()
                #form.project.choices.insert(0,("", "Ingen prosjekt valgt"))
    #else:
        #form = webforms.AddApartmentNoProjectForm()
        #form.project.choices.insert(0,("", "Ingen prosjekt valgt"))

    # Hvis innsending av endringer
    if request.method == "POST":
        if form.validate_on_submit():
            # Hvis prosjekter eksisterer
            if projects:
                # Hvis man velger "ingen prosjekt"
                if not request.form["project"]:
                    apartment.apartmenttype_id = None
                    if apartment.apartmenttype:
                        apartment.apartmenttype.remove(current_apartmenttype)
                    apartment.project_id = None
                else:
                    apartment.project_id = request.form["project"]
                    # Hvis prosjekt er satt
                    if current_apartment_project:
                        # Hvis valgt prosjekt skal overskrive gjeldene
                        if int(current_apartment_project.id) is not int(request.form["project"]): 
                            apartment.apartmenttype_id = None
                            if apartment.apartmenttype:
                                apartment.apartmenttype.remove(current_apartmenttype)
                        else:
                            apartment.apartmenttype_id = request.form["apartmenttype"]
                            if apartment.apartmenttype:
                                apartment.apartmenttype.remove(current_apartmenttype)
                            apartment.apartmenttype.append(Apartmenttype.query.filter_by(id=request.form["apartmenttype"]).first())
            else:
                apartment.apartmenttype_id = None
                if apartment.apartmenttype:
                    apartment.apartmenttype.remove(current_apartmenttype)
                apartment.project_id = None
            db.session.commit()
            flash("User updated!")
            return redirect(url_for("apartments.apartments_list"))    
        else:
            flash("Error apartment")
            return redirect(url_for("apartments.apartments_list"))
    
    return render_template("apartment_edit.html", apartment_id=apartment_id, id=id, form=form, slug=slug, projects=projects, apartmenttypes=apartmenttypes, apartmentdata=apartment_data)

# Sletting av leilighet
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