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

customers_bp = Blueprint('customers', __name__)
app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:12wsxdr56@localhost:3306/eCommerce'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False 

db = SQLAlchemy(app)  


from app import db 

class CustomerSchema(Schema):
    name = fields.Str(required=True)
    email = fields.Email(required=True)
    phone = fields.Str()
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

if __name__ == '__main__':
    with app.app_context(): 
        db.create_all()  
    app.run(debug=True)

