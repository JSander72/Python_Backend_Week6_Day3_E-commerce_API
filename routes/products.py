from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.ext.declarative import declarative_base
from flask_marshmallow import Marshmallow 
from flask import Blueprint, jsonify, request
from marshmallow import Schema, fields

app = Flask(__name__)
Base = declarative_base()

db = SQLAlchemy(app, model_class= Base)
ma = Marshmallow(app)

products_bp = Blueprint('products', __name__)

class ProductSchema(Schema):
    name = fields.Str(required=True)
    price = fields.Float(required=True)
    stock_level = fields.Int(required=True)

db = SQLAlchemy()

class Product(db.Model):
    __tablename__ = 'products'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    price = db.Column(db.Float, nullable=False)
    stock_level = db.Column(db.Integer, nullable=False)
    order_items = db.relationship('OrderItem', backref='product', lazy=True)
    def __repr__(self):
        return f'<Product {self.name}>'