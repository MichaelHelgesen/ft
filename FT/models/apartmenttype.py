from FT import db
from datetime import datetime
from flask_login import UserMixin
from sqlalchemy.orm import declarative_mixin
#from FT.models import products_collections

@declarative_mixin
class HasSlug:
    slug_target_column = "name"
    slug = db.Column(
        db.String,
        unique=True,
        nullable=False,
    )

""" apartments_apartmenttypes = db.Table("apartments_apartmenttypes",
db.Column("apartmenttypes_id", db.Integer, db.ForeignKey("apartmenttype.id")),
db.Column("apartments_id", db.String, db.ForeignKey("apartments.id"))
)
 """

class Apartmenttype(HasSlug, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    project_id = db.Column(db.Integer, db.ForeignKey('project.id'))
    #apartment = db.relationship("Apartment", secondary=apartments_apartmenttypes, backref=db.backref('apartmenttype', lazy='dynamic'))

    def __repr__(self):
        return '<Apartmenttype %r>' % self.name
    
    def __str__(self):
        return self.name
    
    def __unicode__(self):
        return self.name