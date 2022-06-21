class MarketDataOrder:

    def __init__(self, json):
        self.result = {}
        self.price = self.result['price'] = json["price"]
        self.quantity = self.result['quantity'] = json["quantity"]

    def __str__(self):
        return str(self.result)

    def __repr__(self):
        return str(self.result)
