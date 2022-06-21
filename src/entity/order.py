import random

from src.enums.order_type import OrderType


class Order:

    def __init__(self, json=None):
        self.result = {}
        if json is None:
            self.default()
        else:
            self.id = json.get('id')
            self.price = json.get('price')
            self.quantity = json.get('quantity')
            self.side = json.get('side')

    @property
    def id(self):
        return self._id

    @id.setter
    def id(self, value):
        self.result['id'] = self._id = str(value) if value is not None else None

    def set_id(self, value):
        self.id = value
        return self

    @property
    def price(self):
        return self._price

    @price.setter
    def price(self, value):
        self.result['price'] = self._price = str(value) if value is not None else None

    def set_price(self, value):
        self.price = value
        return self

    @property
    def quantity(self):
        return self._quantity

    @quantity.setter
    def quantity(self, value):
        self.result['quantity'] = self._quantity = str(value)

    def set_quantity(self, value):
        self.quantity = value
        return self

    @property
    def side(self):
        return OrderType(self._side)

    @side.setter
    def side(self, value):
        self.result['side'] = self._side = value

    def set_side(self, value):
        self.side = value.value
        return self

    def default(self):
        self.set_id(random.randrange(1, 10000))\
            .set_price(random.randrange(1, 10000))\
            .set_quantity(random.randrange(1, 10000))\
            .set_side(random.choice(list(OrderType)))
        return self

    def json(self):
        return self.result

    def __str__(self):
        return str(self.json())

    def __repr__(self):
        return str(self.json())
