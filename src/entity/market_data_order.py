

class MarketDataOrder:

    def __init__(self, json):
        self.result = {}
        self.price = self.result['price'] = json["price"]
        self.quantity = self.result['quantity'] = json["quantity"]

    def json(self):
        return self.result

    def __str__(self):
        return self.json()
