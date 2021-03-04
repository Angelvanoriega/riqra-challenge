import os
import logging
from flask import Flask, request
from src.auth.resources import User
from src.dbadmin.resources import DB
from src.catalog.resources import Product

logger = logging.getLogger()
logger.setLevel(logging.DEBUG)

# create and configure the app
app = Flask(__name__, instance_relative_config=True)
app.config.from_mapping(
    SECRET_KEY='dev',
    DATABASE=os.path.join(app.instance_path, 'flaskr.sqlite'),
)

app.config.from_pyfile('config.py', silent=True)

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# ensure the instance folder exists
try:
    os.makedirs(app.instance_path)
except OSError:
    pass


@app.errorhandler(404)
def page_not_found(e):
    return "<h1>404</h1><p>The resource could not be found.</p>", 404


@app.route('/api/v1/resources/reset_db', methods=['GET'])
def reset():
    db = DB()
    return db.reset()


@app.route('/api/v1/resources/auth/login', methods=['POST'])
def login():
    email = request.form.get("email")
    password = request.form.get("password")
    user = User(email, password)
    return user.login()


@app.route('/api/v1/resources/catalog/product/search', methods=['GET'])
def product_search():
    term = request.args.get("term")
    product = Product()
    product.term = term
    return {'data': product.search()}


@app.route('/api/v1/resources/catalog/product/list', methods=['GET'])
def product_list():
    supplier = request.args.get("supplier")
    product = Product()
    product.supplier = supplier
    return {'data': product.list()}
