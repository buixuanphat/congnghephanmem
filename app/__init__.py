from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from urllib.parse import quote

app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = "mysql+pymysql://root:%s@localhost/manadb?charset=utf8mb4" % quote("123456")
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["MIN_AGE"]=15
app.config["MAX_AGE"]=20

db = SQLAlchemy(app)