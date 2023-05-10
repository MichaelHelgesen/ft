from FT import db
from datetime import datetime
from flask_login import UserMixin
from sqlalchemy.orm import declarative_mixin

@declarative_mixin
class HasSlug:
    slug_target_column = "name"
    slug = db.Column(
        db.String,
        unique=True,
        nullable=False,
    )

apartments_apartmenttypes = db.Table("apartments_apartmenttypes",
db.Column("apartments_id", db.String, db.ForeignKey("apartments.id")),
db.Column("apartmenttypes_id", db.Integer, db.ForeignKey("apartmenttype.id"))
)

class Apartments(HasSlug, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    apartment_id = db.Column(db.String(200), nullable=False)
    project_id = db.Column(db.Integer, db.ForeignKey('project.id'))
    apartmenttype_id = db.Column(db.Integer, db.ForeignKey('apartmenttype.id'))
    users = db.relationship('Users', backref='apartments')
    apartmenttype = db.relationship("Apartmenttype", secondary=apartments_apartmenttypes, backref=db.backref('apartments', lazy='dynamic'))
