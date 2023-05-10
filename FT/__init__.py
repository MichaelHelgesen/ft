from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
from tablib import Dataset
import flask_excel as excel
# create the extension
db = SQLAlchemy()

#Create a Flask Instance
app = Flask(__name__)
excel.init_excel(app)
# configure the SQLite database, relative to the app instance folder
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///ft.db"
# initialize the app with the extension
db.init_app(app)

# Definisjon av standard loginside
login_manager = LoginManager()
login_manager.login_view = 'login.user_login'
login_manager.init_app(app)

#Importer modeller for å opprette database
from .models.add_user import Users
from .models.projects import Project
from .models.apartments import Apartments
from .models.products import Products
from .models.apartmenttype import Apartmenttype
from .models.room import Room
#from .models.products_collections import products_collections
#from .models.collections import Collections


admin = Admin(app)
# Admin-panel /admin
class UserView(ModelView):
    column_hide_backrefs = False
    can_export = True
    export_types = ['csv', "xls"]
    column_auto_select_related = True
    column_list = ("name", 'username', "email", "role", "date_added")
    
admin.add_view(UserView(Users, db.session))

@login_manager.user_loader
def load_user(user_id):
    # since the user_id is just the primary key of our user table, use it in the query for the user
    return Users.query.get(int(user_id))

with app.app_context():
    db.create_all()

app.secret_key = "hello"

import FT.views

if __name__ == '__main__':
    app.run(debug=True, use_reloader=True)