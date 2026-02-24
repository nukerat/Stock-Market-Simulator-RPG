import random

class MarketItem:
    def __init__(self, name, base_price, volatility):
        self.name = name
        self.base_price = base_price
        self.volatility = volatility
        self.price = base_price

    def update_price(self):
        change = random.randint(-self.volatility, self.volatility)
        self.price = max(1, self.price + change)
