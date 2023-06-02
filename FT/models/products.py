from FT import db
from datetime import datetime
from flask_login import UserMixin
from sqlalchemy.orm import declarative_mixin



@declarative_mixin
class HasSlug:
    #slug_target_column = "nrf" + "-" + "produktnavn"
    slug = db.Column(
        db.String,
        unique=True,
        nullable=False,
    )


class Products(HasSlug, db.Model):
    #id = db.Column(db.Integer, primary_key=True)
    nrf = db.Column(db.String(100), nullable=False, primary_key=True, unique=True)
    leverandor = db.Column(db.String)
    hovedkategori = db.Column(db.String)
    pris = db.Column(db.Integer)
    underkategori = db.Column(db.String)
    kategori = db.Column(db.String)
    produktnavn = db.Column(db.String)
    beskrivelse = db.Column(db.Text)
    mal = db.Column(db.String)
    farge = db.Column(db.String)
    enhet = db.Column(db.String)

    def __str__(self):
        return self.nrf
    
    def __unicode__(self):
        return self.nrf
