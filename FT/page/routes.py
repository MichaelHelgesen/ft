from flask import Blueprint, render_template

page = Blueprint('page', __name__, static_folder="static", template_folder="templates")

@page.route('/')
def index():
    return render_template("index.html")