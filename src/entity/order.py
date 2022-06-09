import random

from src.enums.order_type import OrderType


class Order:

    def __init__(self, json=None):
        self.result = {}
        if json is None:
            self.default()
        else:
            self.set_id(json.get('id'))\
                .set_price(json.get('price'))\
                .set_quantity(json.get('quantity'))\
                .set_side(OrderType(json["side"]))

    def set_id(self, id=random.randrange(1, 10000)):
        self.result['id'] = self.id = id
        return self

    def set_price(self, price=random.randrange(1, 10000)):
        self.result['price'] = self.price = price
        return self

    def set_quantity(self, quantity=random.randrange(1, 10000)):
        self.result['quantity'] = self.quantity = quantity
        return self

    def set_side(self, side=random.choice(list(OrderType))):
        self.side = side
        self.result['side'] = side.value
        return self

    def default(self):
        self.set_id().set_price().set_quantity().set_side()
        return self

    def json(self):
        return self.result

    def __str__(self):
        return self.json()
