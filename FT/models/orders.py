from FT import db
from datetime import datetime
from flask_login import UserMixin
from sqlalchemy.orm import declarative_mixin
from sqlalchemy.sql import func

order_statuses = db.Table("order_statuses",
    db.Column("orders_id", db.Integer, db.ForeignKey("orders.id", ondelete='CASCADE')),
    db.Column("status_id", db.Integer, db.ForeignKey("status.id", ondelete='CASCADE'))
)

class Orders(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    leilighet_id = db.Column(db.Integer, db.ForeignKey('apartments.id'))
    leilighet_navn = db.Column(db.String)
    dato = db.Column(db.DateTime(timezone=True), server_default=func.now())
    status = db.relationship("Status", secondary=order_statuses, backref=db.backref('orders', lazy='dynamic'))
    standardprodukter = db.Column(db.Boolean)

    def __repr__(self):
        return '<Orders %r>' % self.id
    
    def __str__(self):
        return self.id
    
    def __unicode__(self):
        return self.id    

class Status(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(40))
    description = db.Column(db.String(255))
    
    def __str__(self):
        return self.name
    
    def __unicode__(self):
        return self.name

class Ordreoversikt(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    ordre_id = db.Column(db.Integer, db.ForeignKey('orders.id'))
    produkt_id = db.Column(db.String(100), db.ForeignKey('products.nrf'))
    antall = db.Column(db.Integer)
    pris = db.Column(db.Integer)
    rom_id = db.Column(db.Integer, db.ForeignKey('room.id'))
    kategori_id = db.Column(db.Integer, db.ForeignKey('category.id'))
    
    def __str__(self):
        return self.id
    
    def __unicode__(self):
        return self.id