from market.item import MarketItem

class Market:
    def __init__(self):
        self.items = [
            #name, base price, volatiliy
            MarketItem("Wheat", 10, 2),
            MarketItem("Iron", 50, 5),
            MarketItem("Fish", 8, 2)
        ]

    def update_day(self):
        for item in self.items:
            item.update_price()
