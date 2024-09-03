import os
print(os.getcwd())
import sys
print(sys.path)

from flask import Config, Flask, Blueprint, jsonify, request
from flask_marshmallow import Marshmallow
from flask_sqlalchemy import SQLAlchemy
from marshmallow import Schema, fields, ValidationError
import mysql.connector 

# Define Flask app and SQLAlchemy
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:12wsxdr56@localhost:3306/eCommerce'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False 
db = SQLAlchemy(app)
ma = Marshmallow(app)

# Define schemas
class MemberSchema(ma.Schema):
    class Meta:
        fields = ('customer', 'order', 'product', 'bonus')

class CustomerSchema(Schema):
    name = fields.Str(required=True)
    email = fields.Email(required=True)
    phone = fields.Str()

from customer import Customer

customers_bp = Blueprint('customers', __name__)

def get_db_connection():
    connection = mysql.connector.connect(
        host="localhost",
        user="root",
        password="12wsxdr56",
        database="eCommerce"
    )
    return connection

# Test connection
with get_db_connection() as conn:
    print("Database connected successfully!")

member_schema = MemberSchema()
members_schema = MemberSchema(many=True)

app.config.from_object(Config)

@app.route('/')
def home():
    return "Welcome to the E-commerce API"

class CustomerSchema(Schema):
    name = fields.Str(required=True)
    email = fields.Email(required=True)
    phone = fields.Str()

@customers_bp.route('/customers', methods=['GET'])
def get_customers():
    customers = Customer.query.all()
    schema = CustomerSchema(many=True)
    return jsonify(schema.dump(customers))

@customers_bp.route('/customers/<int:customer_id>', methods=['GET'])
def get_customer(customer_id):
    customer = Customer.query.get_or_404(customer_id)
    schema = CustomerSchema()
    return jsonify(schema.dump(customer))

# Create customer
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

# Update customer
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

# Delete customer
@customers_bp.route('/customers/<int:customer_id>', methods=['DELETE'])
def delete_customer(customer_id):
    customer = Customer.query.get_or_404(customer_id)
    db.session.delete(customer)
    db.session.commit()
    return '', 204

if __name__ == "__main__":
    app.run(debug=True)

