from flask import Blueprint, jsonify, request
from app import Order, OrderItem, db, Customer, Product
from marshmallow import Schema, fields
from datetime import datetime

orders_bp = Blueprint('orders', __name__)

class OrderSchema(Schema):
    customer_id = fields.Int(required=True)
    status = fields.Str(required=True)
    order_date = fields.DateTime(required=True)
    customer = fields.Nested('CustomerSchema', only=['id', 'name'])
    items = fields.Nested('OrderItemSchema', many=True, exclude=['order'])

    
# Get all orders for a customer
@orders_bp.route('/customers/<int:customer_id>/orders', methods=['GET'])
def get_customer_orders(customer_id):
    customer = Customer.query.get_or_404(customer_id) 
    orders = customer.orders
    schema = OrderSchema(many=True)
    return jsonify(schema.dump(orders))

# Cancel order
@orders_bp.route('/orders/<int:order_id>/cancel', methods=['PUT'])
def cancel_order(order_id):
    order = Order.query.get_or_404(order_id)

    # Check if order can be canceled
    if order.order_date < datetime.now():  
        return jsonify({"error": "Cannot cancel order, it's already in the past"}), 400

    # Mark canceled 
    order.status = 'canceled'  
    db.session.commit()

    return jsonify({"message": "Order canceled successfully"})

# total price of an order
@orders_bp.route('/orders/<int:order_id>/total', methods=['GET'])
def get_order_total(order_id):
    order = Order.query.get_or_404(order_id)
    total_price = 0
    for item in order.items:
        total_price += item.product.price * item.quantity
    return jsonify({"total_price": total_price})

# Restock a product 
@orders_bp.route('/products/<int:product_id>/restock', methods=['PUT'])
def restock_product(product_id):
    product = Product.query.get_or_404(product_id)
    try:
        quantity = int(request.json.get('quantity'))
        if quantity <= 0:
            raise ValueError("Restock quantity must be positive")
        product.stock_level += quantity
        db.session.commit()
        return jsonify({"message": f"Product {product.name} restocked successfully"})
    except (KeyError, ValueError) as e:
        return jsonify({"error": str(e)}), 400
