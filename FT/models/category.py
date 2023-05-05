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


products_category = db.Table("products_category",
    db.Column("products_id", db.String, db.ForeignKey("products.nrf")),
    db.Column("category_id", db.Integer, db.ForeignKey("category.id"))
)

class Category(HasSlug, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    room_id = db.Column(db.Integer, db.ForeignKey('room.id'))
    product = db.relationship("Products", secondary=products_category, backref=db.backref('category', lazy='dynamic'))

    def __repr__(self):
        return '<Category %r>' % self.name
    
    def __str__(self):
        return self.name
    
    def __unicode__(self):
        return self.name