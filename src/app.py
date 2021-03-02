import os
import logging
from flask import Flask

logger = logging.getLogger()
logger.setLevel(logging.DEBUG)

# create and configure the app
app = Flask(__name__, instance_relative_config=True)
app.config.from_mapping(
    SECRET_KEY='dev',
    DATABASE=os.path.join(app.instance_path, 'flaskr.sqlite'),
)

app.config.from_pyfile('config.py', silent=True)

# ensure the instance folder exists
try:
    os.makedirs(app.instance_path)
except OSError:
    pass


@app.errorhandler(404)
def page_not_found(e):
    return "<h1>404</h1><p>The resource could not be found.</p>", 404


@app.route('/api/v1/resources/hello')
def hello():
    app.logger.debug('Processing default request')
    return 'Hello, World!'
