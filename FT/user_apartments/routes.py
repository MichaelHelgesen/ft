from flask import Blueprint, render_template
from flask_login import login_user, login_required, current_user, logout_user
from FT.models.apartments import Apartments
from FT.models.room import Room
from FT.models.collections import Collections, products_collections
from FT.models.category import Category
from FT.models.apartmenttype import Apartmenttype


user_apartments = Blueprint('user_apartments', __name__, static_folder="static",
                  template_folder="templates")

# Landingsside for alle brukerens leiligheter
@user_apartments.route('/apartment', methods=["GET", "POST"])
@login_required
def apartment_list():
        user_apartments = Apartments.query.filter_by(id = current_user.apartment_id).all()
        return render_template("apartment.html", name=current_user, user_apartments=user_apartments)

@user_apartments.route('/apartment/<string:apartment>', methods=["GET", "POST"])
@login_required
def apartment_rooms(apartment):
        user_apartments = Apartments.query.filter_by(id = current_user.apartment_id).first()
        print(user_apartments.apartmenttype)
        #room_id = Room.query.filter(Room.slug.like(room), Room.apartmenttype.like(apartmenttype_id.id)).first()
        user_apartmenttype = Apartments.query.filter_by(apartmenttype = user_apartments).first()
        #user_rooms = Room.query.filter_by(apartmenttype = user_apartments).first()
        return render_template("apartment_rooms.html", user_rooms=user_rooms, apartment=apartment)

@user_apartments.route('/apartment/<string:apartment>/<string:room>', methods=["GET", "POST"])
@login_required
def apartment_category(apartment, room):
        apartment_id = Apartments.query.filter_by(id = current_user.apartment_id).first()
        #room_id = Room.query.filter_by(apartmenttype = )
        #room_categories = Category.query.filter_by(room_id = room.id).all()
        return render_template("categories.html", apartment=apartment, room=room)
