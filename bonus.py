from flask import Flask
from flask import Blueprint, jsonify, request
from .models import Order, OrderItem, db, Customer
from marshmallow import Schema, fields, ValidationError, post_load
from datetime import datetime

orders_bp = Blueprint('orders', __name__)

app = Flask(__name__)
@app.route('/')
def home():
    return "Welcome to the E-commerce API"

class OrderSchema(Schema):
    id = fields.Int(dump_only=True)  
    customer_id = fields.Int(required=True)
    order_date = fields.DateTime(dump_only=True)
    items = fields.Nested('OrderItemSchema', many=True)

    @post_load
    def make_order(self, data, **kwargs):
        return Order(**data)

class OrderItemSchema(Schema):
    id = fields.Int(dump_only=True)
    order_id = fields.Int(dump_only=True)
    product_id = fields.Int(required=True)
    quantity = fields.Int(required=True)

    @post_load
    def make_order_item(self, data, **kwargs):
        return OrderItem(**data)

# Get all orders for specific customer
@orders_bp.route('/customers/<int:customer_id>/orders', methods=['GET'])
def get_customer_orders(customer_id):
    customer = Customer.query.get_or_404(customer_id)  # does customer exists
    orders = customer.orders
    schema = OrderSchema(many=True)
    return jsonify(schema.dump(orders))

# Cancel an order
@orders_bp.route('/orders/<int:order_id>/cancel', methods=['PUT'])
def cancel_order(order_id):
    order = Order.query.get_or_404(order_id)

    # can it be cancelled or not
    if order.order_date < datetime.now(): 
        return jsonify({"error": "Cannot cancel order, it's already in the past"}), 400

    # Mark order as canceled 
    order.status = 'canceled' 
    db.session.commit()

    return jsonify({"message": "Order canceled successfully"})
