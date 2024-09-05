import os
print(os.getcwd())
import sys
print(sys.path)

from flask import Config, Flask, Blueprint, jsonify, request
from flask_marshmallow import Marshmallow
from flask_sqlalchemy import SQLAlchemy
from marshmallow import Schema, fields, ValidationError
import mysql.connector 
from sqlalchemy.ext.declarative import declarative_base
from customer import CustomerSchema, Customer
from products import ProductSchema, Product
from orders import OrderItem, OrderSchema, Order
from datetime import date
from dataclasses import dataclass





# Define Flask app and SQLAlchemy
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:12wsxdr56@localhost:3306/eCommerce'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True 
db = SQLAlchemy(app)
ma = Marshmallow(app)

# Define schemas
class MemberSchema(ma.Schema):
    class Meta:
        fields = ('customer', 'order', 'product', 'bonus')

customers_bp = Blueprint('customers', __name__)
orders_bp = Blueprint('orders', __name__) 
products_bp = Blueprint('products', __name__)


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

# Order Routes
@orders_bp.route('/orders', methods=['GET'])
def get_orders():
    orders = Order.query.all()
    schema = OrderSchema(many=True)
    return jsonify(schema.dump(orders))

@orders_bp.route('/orders/<int:order_id>', methods=['GET'])
def get_order(order_id):
    order = Order.query.get_or_404(order_id)
    schema = OrderSchema()
    return jsonify(schema.dump(order))

# CREATE (POST)
@orders_bp.route('/orders', methods=['POST'])
def create_order():
    try:
        data = OrderSchema().load(request.json)

        # Create order
        new_order = Order(customer_id=data['customer_id'])
        db.session.add(new_order)
        db.session.flush()  
        
        for item_data in data['items']:
            new_item = OrderItem(
                order_id=new_order.id, 
                product_id=item_data['product_id'], 
                quantity=item_data['quantity']
            )
            db.session.add(new_item)

        db.session.commit()
        return jsonify(OrderSchema().dump(new_order)), 201

    except ValidationError as err:
        return jsonify(err.messages), 400

# UPDATE (PUT)
@orders_bp.route('/orders/<int:order_id>', methods=['PUT'])
def update_order(order_id):
    order = Order.query.get_or_404(order_id)
    try:
        data = OrderSchema(partial=True).load(request.json)  
        
        if 'customer_id' in data:
            order.customer_id = data['customer_id']
        
        if 'items' in data:
            db.session.commit()
        return jsonify(OrderSchema().dump(order))

    except ValidationError as err:
        return jsonify(err.messages), 400

# DELETE
@orders_bp.route('/orders/<int:order_id>', methods=['DELETE'])
def delete_order(order_id):
    order = Order.query.get_or_404(order_id)
    db.session.delete(order) 
    db.session.commit()
    return '', 204 


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
@products_bp.route('/products', methods=['POST'])
def create_product():
    """Creates a new product."""
    try:
        data = request.get_json()
        product_schema = ProductSchema()
        product = product_schema.load(data)
        new_product = Product(**product)
        db.session.add(new_product)
        db.session.commit()
        return jsonify(product_schema.dump(new_product)), 201
    except ValidationError as err:
        return jsonify(err.messages), 400

@products_bp.route('/products/<int:product_id>', methods=['PUT'])
def update_product(product_id):
    """Updates an existing product."""
    product = Product.query.get_or_404(product_id)
    try:
        data = request.get_json()
        product_schema = ProductSchema()
        updated_product = product_schema.load(data)
        product.name = updated_product['name']
        product.price = updated_product['price']
        product.stock_level = updated_product['stock_level']
        db.session.commit()
        return jsonify(product_schema.dump(product))
    except ValidationError as err:
        return jsonify(err.messages), 400

@products_bp.route('/products/<int:product_id>', methods=['DELETE'])
def delete_product(product_id):
    """Deletes a product."""
    product = Product.query.get_or_404(product_id)
    db.session.delete(product)
    db.session.commit()
    return '', 204

app.register_blueprint(customers_bp)
app.register_blueprint(orders_bp)
app.register_blueprint(products_bp)


if __name__ == '__main__':
    with app.app_context(): 
        db.create_all()  
    app.run(debug=True)


