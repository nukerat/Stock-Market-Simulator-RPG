import json
import os
from market.item import MarketItem

# Use absolute paths to avoid relative path issues
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
SAVE_FOLDER = os.path.join(BASE_DIR, "save")
SAVE_FILE = os.path.join(SAVE_FOLDER, "save1.json")

def save_game(player, market=None):
    """
    Save player and optional market state to JSON.
    """
    if not os.path.exists(SAVE_FOLDER):
        os.makedirs(SAVE_FOLDER)

    data = {
        "player": {
            "x": player.x,
            "y": player.y,
            "gold": player.gold,
            "inventory": player.inventory,
            "history": player.history
        }
    }

    if market is not None:
        data["market"] = []
        for item in market.items:
            data["market"].append({
                "name": item.name,
                "price": item.price,
                "base_price": item.base_price,
                "volatility": item.volatility
            })

    with open(SAVE_FILE, "w") as f:
        json.dump(data, f)
    print("Game saved!")

def load_game(player, market=None):
    """
    Load player and optional market state from JSON.
    """
    if not os.path.exists(SAVE_FILE):
        print("No save file found.")
        return False

    with open(SAVE_FILE, "r") as f:
        data = json.load(f)

    # Load player
    pdata = data.get("player", {})
    player.x = pdata.get("x", player.x)
    player.y = pdata.get("y", player.y)
    player.gold = pdata.get("gold", player.gold)
    player.inventory = pdata.get("inventory", player.inventory)
    player.history = pdata.get("history", [])

    # Load market if provided
    if market is not None and "market" in data:
        market.items = []
        for item_data in data["market"]:
            item = MarketItem(
                item_data["name"],
                item_data.get("base_price", 10),
                item_data.get("volatility", 2)
            )
            item.price = item_data.get("price", item.price)
            market.items.append(item)

    print("Game loaded!")
    return True
