import random

from src.enums.order_type import OrderType


class Order:

    def __init__(self, json=None):
        self.result = {}
        if json is None:
            self.id = None
            self.price = None
            self.quantity = None
            self.side = None
        else:
            self.set_id(json["id"] if not (json.get('id') is None) else None)\
                .set_price(json["price"] if not (json.get('price') is None) else None)\
                .set_quantity(json["quantity"] if not (json.get('quantity') is None) else None)\
                .set_side(OrderType(json["side"]) if not (json.get('side') is None) else None)

    def set_id(self, id=random.randrange(1, 10000)):
        self.result['id'] = id
        self.id = id
        return self

    def set_price(self, price=random.randrange(1, 10000)):
        self.result['price'] = price
        self.price = price
        return self

    def set_quantity(self, quantity=random.randrange(1, 10000)):
        self.result['quantity'] = quantity
        self.quantity = quantity
        return self

    def set_side(self, side=random.choice(list(OrderType))):
        self.result['side'] = side.value
        self.side = side
        return self

    def default(self):
        self.set_id().set_price().set_quantity().set_side()
        return self

    def build(self):
        return self.result

    def __str__(self):
        return self.result.__str__()
