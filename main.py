from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask import Blueprint, jsonify, request
from models import db 
from marshmallow import Schema, fields, ValidationError
from routes.customer import Customer


customers_bp = Blueprint('customers', __name__)
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI']='mysql://root:12wsxdr56@localhost:3306/eCommerce'

db = SQLAlchemy(app)

# Create an instance of the Flask class
@app.route('/')
def home():
    return "Welcome to the E-commerce API"

# Schema for validation
class CustomerSchema(Schema):
    name = fields.Str(required=True)
    email = fields.Email(required=True)
    phone = fields.Str()

# Get all customers
@customers_bp.route('/customers', methods=['GET'])
def get_customers():
    customers = Customer.query.all()
    schema = CustomerSchema(many=True)
    return jsonify(schema.dump(customers))

# Get a single customer by ID
@customers_bp.route('/customers/<int:customer_id>', methods=['GET'])
def get_customer(customer_id):
    customer = Customer.query.get_or_404(customer_id)
    schema = CustomerSchema()
    return jsonify(schema.dump(customer))

# Create a new customer
@customers_bp.route('/customers', methods=['POST'])
def create_customer():
    try:
        schema = CustomerSchema()
        customer_data = schema.load(request.json)
        new_customer = Customer(**customer_data)
        db.session.add(new_customer)
        db.session.commit()
        return jsonify(schema.dump(new_customer)), 201
    except ValidationError as err:
        return jsonify(err.messages), 400

# Update an existing customer
@customers_bp.route('/customers/<int:customer_id>', methods=['PUT'])
def update_customer(customer_id):
    customer = Customer.query.get_or_404(customer_id)
    try:
        schema = CustomerSchema()
        customer_data = schema.load(request.json)
        for key, value in customer_data.items():
            setattr(customer, key, value)
        db.session.commit()
        return jsonify(schema.dump(customer))
    except ValidationError as err:
        return jsonify(err.messages), 400

# Delete a customer
@customers_bp.route('/customers/<int:customer_id>', methods=['DELETE'])
def delete_customer(customer_id):
    customer = Customer.query.get_or_404(customer_id)
    db.session.delete(customer)
    db.session.commit()
    return '', 204