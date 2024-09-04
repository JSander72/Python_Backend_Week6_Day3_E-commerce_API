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

#moved to customer, products, & orders routes to appropriate file for easier reading

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

if __name__ == "__main__":
    app.run(debug=True)

