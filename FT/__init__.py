from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager

# create the extension
db = SQLAlchemy()

#Create a Flask Instance
app = Flask(__name__)
# configure the SQLite database, relative to the app instance folder
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///ft.db"
# initialize the app with the extension
db.init_app(app)

login_manager = LoginManager()
login_manager.login_view = 'user_profile'
login_manager.init_app(app)

from .models.add_user import Users

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