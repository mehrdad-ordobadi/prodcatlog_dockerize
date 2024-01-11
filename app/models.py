# app/models.py
from flask_sqlalchemy import SQLAlchemy
from database import db

class Item(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True, nullable=False)

    def __repr__(self):
        return f'<Item {self.name}>'
