

# TODO
class MarketDataOrder:

    def __init__(self, json):
        self.result = {}

        self.price = json["price"]
        self.result['price'] = self.price

        self.quantity = json["quantity"]
        self.result['quantity'] = self.quantity

    def build(self):
        return self.result

    def __str__(self):
        return self.result.__str__()
