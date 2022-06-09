from src.entity.market_data_order import MarketDataOrder


class MarketData:

    def __init__(self, json):
        self.result = {'asks': list(), 'bids': list()}
        self.result['asks'].extend(MarketDataOrder(element) for element in json.get('asks'))
        self.result['bids'].extend(MarketDataOrder(element) for element in json.get('bids'))

    def build(self):
        return self.result

    def __str__(self):
        return self.result.__str__()
