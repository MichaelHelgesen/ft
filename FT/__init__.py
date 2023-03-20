from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from flask_sqlalchemy import SQLAlchemy


# create the extension
db = SQLAlchemy()

#Create a Flask Instance
app = Flask(__name__)
from .models.add_app import App
# configure the SQLite database, relative to the app instance folder
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///ft.db"
# initialize the app with the extension
db.init_app(app)

with app.app_context():
    db.create_all()


app.secret_key = "hello"

import FT.views

if __name__ == '__main__':
    app.run(debug=True, use_reloader=True)