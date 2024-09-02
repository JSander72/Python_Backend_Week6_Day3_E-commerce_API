from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask import Blueprint, jsonify, request
from ..models import db


customers_bp = Blueprint('customers', __name__)
app = Flask(__name__)
db = SQLAlchemy()

class Customer(db.Model):
    __tablename__ = 'customers'  
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False) 
    phone = db.Column(db.String(20))
    orders = db.relationship('Order', backref='customer', lazy=True)
    accounts = db.relationship('CustomerAccount', backref='customer', lazy=True)

    def __repr__(self):
        return f'<Customer {self.name}>'
    
class CustomerAccount(db.Model):
    __tablename__ = 'customer_accounts'
    id = db.Column(db.Integer, primary_key=True)
    customer_id = db.Column(db.Integer, db.ForeignKey('customers.id'), nullable=False)
    username  = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(120), nullable=False) 

    def __repr__(self):
        return f'<CustomerAccount {self.username}>'

