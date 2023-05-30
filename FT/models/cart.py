from FT import db
from datetime import datetime
from flask_login import UserMixin
from sqlalchemy.orm import declarative_mixin



class Cart(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    leilighet_id = db.Column(db.Integer, db.ForeignKey('apartments.id'))
    produkt_id = db.Column(db.String, db.ForeignKey('products.nrf'))
    antall = db.Column(db.Integer)
    rom = db.Column(db.Integer, db.ForeignKey('room.id'))
    kategori = db.Column(db.Integer, db.ForeignKey('category.id'))

    def __int__(self):
        return self.id
    
    def __unicode__(self):
        return self.id
