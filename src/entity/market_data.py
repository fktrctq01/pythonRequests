from src.entity.market_data_order import MarketDataOrder


class MarketData:

    def __init__(self, json):
        self.result = {'asks': list(), 'bids': list()}

        self.asks = [MarketDataOrder(element) for element in json.get('asks')]
        self.result['asks'].extend(self.asks)

        self.bids = [MarketDataOrder(element) for element in json.get('bids')]
        self.result['bids'].extend(self.bids)

    def __str__(self):
        return str(self.result)

    def __repr__(self):
        return str(self.result)
