from src.entity.market_data_order import MarketDataOrder


class MarketData:

    def __init__(self, json):
        self.result = {}

        self.asks = list()
        for element in json.get('asks'):
            self.asks.append(MarketDataOrder(element))
        self.result['asks'] = self.asks

        self.bids = list()
        for element in json.get('bids'):
            self.bids.append(MarketDataOrder(element))
        self.result['bids'] = self.bids

    def build(self):
        return self.result

    def __str__(self):
        return self.result.__str__()
