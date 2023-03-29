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


class Apartments(HasSlug, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    apartment_id = db.Column(db.String(200), nullable=False)
    project_id = db.Column(db.Integer, db.ForeignKey("project.id"))