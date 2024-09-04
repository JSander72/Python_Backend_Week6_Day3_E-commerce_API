
from flask_marshmallow import Marshmallow 
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.ext.declarative import declarative_base
from flask import Blueprint, jsonify
from marshmallow import Schema, fields, ValidationError
from app import db

app = Flask(__name__)
Base = declarative_base()

app.config['SQLALCHEMY_DATABASE_URI'] ='sqlite:///products.db'
db = SQLAlchemy(app, model_class= Base)
ma = Marshmallow(app)
products_bp = Blueprint('products', __name__)

class ProductSchema(Schema):
    name = fields.Str(required=True)
    price = fields.Float(required=True)
    stock_level = fields.Int(required=True)

# db = SQLAlchemy()

class Product(db.Model):
    __tablename__ = 'products'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    price = db.Column(db.Float, nullable=False)
    stock_level = db.Column(db.Integer, nullable=False)
    order_items = db.relationship('OrderItem', backref='product', lazy=True)
    def __repr__(self):
        return f'<Product {self.name}>'    

# Product Routes
@products_bp.route('/products', methods=['GET'])
def get_products():
    products = Product.query.all()
    schema = ProductSchema(many=True)
    return jsonify(schema.dump(products))


@products_bp.route('/products/<int:product_id>', methods=['GET'])
def get_product(product_id):
    product = Product.query.get_or_404(product_id)
    schema = ProductSchema()
    return jsonify(schema.dump(product))

if __name__ == '__main__':
    with app.app_context(): 
        db.create_all()  
    app.run(debug=True)
    
