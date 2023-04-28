from FT import db
from datetime import datetime
from flask_login import UserMixin
import unicodedata

roles_users = db.Table("roles_users",
    db.Column("user_id", db.Integer, db.ForeignKey("users.id")),
    db.Column("role_id", db.Integer, db.ForeignKey("role.id"))
)


# Create database model
class Users(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    username = db.Column(db.String(20), nullable=False)
    email = db.Column(db.String(100), nullable=False, unique=True)
    date_added = db.Column(db.DateTime, default=datetime.utcnow)
    password_hash = db.Column(db.String(128))
    role = db.relationship("Role", secondary=roles_users,backref=db.backref('user', lazy='dynamic'))
    apartment_id = db.Column(db.Integer, db.ForeignKey('apartments.id'))

    def __repr__(self):
        return '<Users %r>' % self.name
    
    def __str__(self):
        return self.name
    
    def __unicode__(self):
        return self.name

class Role(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(40))
    description = db.Column(db.String(255))
    
    

    def __str__(self):
        return self.name
    
    def __unicode__(self):
        return self.name
