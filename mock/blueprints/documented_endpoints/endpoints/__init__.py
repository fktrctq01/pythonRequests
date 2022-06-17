# blueprints/documented_endpoints/endpoints/__init__.py
from flask_restx import Namespace, Resource, fields

namespace = Namespace('endpoints', path='/')

order_model = namespace.model('order', {
    'id': fields.String(
        description='optional param (integer/string, 10000 > id > 0)',
        default="1",
        required=False
    ),
    'price': fields.String(
        description='optional param (double/string, 10000 > price > 0, precision: two decimal places)',
        default="100",
        required=False
    ),
    'quantity': fields.String(
        description='required param (long/string, 10000 > quantity > 0)',
        default="10",
        required=True
    ),
    'side': fields.String(
        description='required param (string - buy or sell)',
        default="sell",
        required=True
    )
})


@namespace.route('/api/order')
class GetAndDelOrder(Resource):

    @namespace.doc(responses={200: 'Success', 400: 'Bad Request', 404: 'Not found'})
    @namespace.param("id", required=True, type=str)
    def get(self):
        """get order by id"""

    @namespace.doc(responses={200: 'Success', 400: 'Bad Request', 404: 'Not found'})
    @namespace.param("id", required=True, type=str)
    def delete(self):
        """delete order by id"""


@namespace.route('/api/order/clean')
class CleanOrder(Resource):

    @namespace.doc(responses={200: 'Success'})
    def get(self):
        """clean orderbook"""


@namespace.route('/api/marketdata')
class GetMarketdata(Resource):

    @namespace.doc(responses={200: 'Success'})
    def get(self):
        """get snapshot of marketdata"""


@namespace.route('/api/order/create')
class CreateOrder(Resource):

    @namespace.expect(order_model, validate=True)
    @namespace.doc(responses={200: 'Success', 400: 'Bad Request', 404: 'Not found'})
    def post(self):
        """create an order"""
