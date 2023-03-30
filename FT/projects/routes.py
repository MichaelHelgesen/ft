from flask import Blueprint, render_template, flash, redirect, url_for, request, jsonify
from FT.forms import webforms
from FT import db, app
import flask_excel as excel
import io
import pandas as pd
from functools import wraps
from FT.models.projects import Project
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, login_required, current_user, logout_user
import csv
import re

projects = Blueprint('projects', __name__, static_folder="static",
                  template_folder="templates")

def str_to_slug(string, delimeter = "-"):
    slug = re.sub(r"[^\w\d\s]", "", string.strip().lower())
    slug = re.sub(" +", " ", slug)
    slug = slug.replace(" ", delimeter)
    return slug

@projects.route('/projects', methods=["GET", "POST"])
def project_list():
    form = webforms.ProjectForm()
    projects = Project.query.all()
    if request.method == "POST":
        if form.validate_on_submit():
            project_name = form.name.data.upper()  
            project = Project.query.filter_by(name = project_name).first()
            if project is None:
                new_project = Project()
                new_project.name = project_name
                new_project.slug = str_to_slug(project_name)
                db.session.add(new_project)
                db.session.commit()
                form.name.data = ""
                flash("project added")
                return redirect(url_for("projects.project_list"))
            else:
                flash("project name already exists")
                return redirect(url_for("projects.project_list"))
        else:
            flash("Something went wrong")
            return render_template("projects.html", form=form)
    return render_template("projects.html", form=form, projects=projects)


@projects.route('/projects/<string:slug>', methods=["GET", "POST"])
def project_edit(slug):
    project = Project.query.filter_by(slug=slug).first()
    form = webforms.UpdateProjectForm()
    form.name.data = project.name.title()
    name = project.name
    if request.method == "POST":
        if form.validate_on_submit():
                project.name = request.form["name"].upper()
                project.slug = str_to_slug(request.form["name"])
                db.session.commit()
                flash("Project updated!")
                return redirect(url_for("projects.project_list"))   
        else:
            flash("Error")
            return redirect(url_for("projects.project_list"))
        
    return render_template("project_edit.html", name=name.title(), slug=slug, form=form)

