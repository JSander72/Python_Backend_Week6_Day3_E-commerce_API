from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask import Blueprint, jsonify, request

class Config:
    SQLALCHEMY_DATABASE_URI ='mysql://root:12wsxdr56@localhost:3306/eCommerce'


app = Flask(__name__)
app.config.from_object(Config)
db = SQLAlchemy(app)

