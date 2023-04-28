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


products_collections = db.Table("products_collections",
    db.Column("products_id", db.String, db.ForeignKey("products.nrf")),
    db.Column("collections_id", db.Integer, db.ForeignKey("collections.id"))
)

class Collections(HasSlug, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    project_id = db.Column(db.Integer, db.ForeignKey('project.id'))
    product = db.relationship("Products", secondary=products_collections, backref=db.backref('collections', lazy='dynamic'))

    def __repr__(self):
        return '<Collections %r>' % self.name
    
    def __str__(self):
        return self.name
    
    def __unicode__(self):
        return self.name