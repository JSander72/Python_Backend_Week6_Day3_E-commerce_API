from flask_sqlalchemy import SQLAlchemy
from flask import Blueprint
from ..app import db
from app import db
from marshmallow import Schema, fields


db = SQLAlchemy()
orders_bp = Blueprint('orders', __name__)

class OrderSchema(Schema):
    customer_id = fields.Int(required=True)

class OrderItemSchema(Schema):
    order_id = fields.Int(required=True)
    product_id = fields.Int(required=True)
    quantity = fields.Int(required=True)




class Order(db.Model):
    __tablename__ = 'orders'
    id = db.Column(db.Integer, primary_key=True) 
    customer_id = db.Column(db.Integer, db.ForeignKey('customers.id'), nullable=False) 
    order_date = db.Column(db.DateTime, nullable=False, default=db.func.now())
    items = db.relationship('OrderItem', backref='order', lazy=True)
    def __repr__(self):
        return f'<Order {self.id}>'

class OrderItem(db.Model):
    __tablename__ = 'order_items'
    id = db.Column(db.Integer, primary_key=True) 
    order_id = db.Column(db.Integer, db.ForeignKey('orders.id'), nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey('products.id'), nullable=False)
    quantity = db.Column(db.Integer, nullable=False) 
    def __repr__(self):
        return f'<OrderItem {self.id}>'