class Player:
    def __init__(self):
        self.x = 400
        self.y = 300
        self.speed = 4
        self.size = 32
        self.gold = 100
        self.inventory = {}  # a dictionary, so item_name: quantity
        self.history = [] #a log of transactions
        

    def move(self, keys):
        if keys["up"]:
            self.y -= self.speed
        if keys["down"]:
            self.y += self.speed
        if keys["left"]:
            self.x -= self.speed
        if keys["right"]:
            self.x += self.speed
            
        # Clamp to screen boundaries
        self.x = max(0, min(self.x, 800 - self.size))
        self.y = max(0, min(self.y, 600 - self.size))
