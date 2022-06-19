# blueprints/documented_endpoints/__init__.py
from flask import Blueprint
from flask_restx import Api
from mock.blueprints.documented_endpoints.endpoints import namespace as orderbook_ns


blueprint = Blueprint('documented_api', __name__, url_prefix='/mock')

api_extension = Api(
    blueprint,
    title='OrderBook mock service',
    version='1.0',
    description='This service allows you to add orders to the order book, delete and view the order book'
)

api_extension.add_namespace(orderbook_ns)
