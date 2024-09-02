from flask import Flask
from flask_marshmallow import Marshmallow
from config import get_db_connection
from flask import Flask, request
from flask_sqlalchemy import SQLAlchemy
from config import Config

app = Flask(__name__)
ma = Marshmallow(app)

class MemberSchema(ma.Schema):
    class Meta:
        fields = ('customer', 'order', 'product', 'bonus')

member_schema = MemberSchema()
members_schema = MemberSchema(many=True)


app.config.from_object(Config)
db = SQLAlchemy(app)
