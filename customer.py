from flask import Config, Flask, request
from flask_sqlalchemy import SQLAlchemy
from flask import Blueprint, jsonify
from marshmallow import Schema, fields, ValidationError
from sqlalchemy.ext.declarative import declarative_base

 

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

from app import db
customers_bp = Blueprint('customers', __name__)

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:12wsxdr56@localhost:3306/eCommerce'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True 
db = SQLAlchemy(app)


class CustomerSchema(Schema):
    name = fields.Str(required=True)
    email = fields.Email(required=True)
    phone = fields.Str()
    
if __name__ == '__main__':
    with app.app_context(): 
        db.create_all()  
    app.run(debug=True)
