from FT import db
from datetime import datetime
from flask_login import UserMixin



products_collections = db.Table("products_collections",
    db.Column("products_id", db.String, db.ForeignKey("products.nrf")),
    db.Column("collections_id", db.Integer, db.ForeignKey("collections.id"))
)