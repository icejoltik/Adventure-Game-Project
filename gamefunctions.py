# gamefunctions.py
# Bryan Strozyk
# 9/28/2025



import random

def purchase_item(itemPrice, startingMoney, quantityToPurchase=1):
    max_affordable = startingMoney // itemPrice
    quantity_purchased = min(quantityToPurchase, max_affordable)
    money_remaining = startingMoney - (itemPrice * quantity_purchased)
    return quantity_purchased, money_remaining

def new_random_monster():
    monster_types = [
        {
            "name": "Goblin",
            "description": "This is a lone goblin. When it notices you, it rushes at you quickly with a sharp dagger drawn.",
            "health_range": (10, 30),
            "power_range": (5, 15),
            "money_range": (50, 150)
        },
        {
            "name": "Vulture",
            "description": "You discover a vulture eating the remains of two orcs that appear to have killed each other.\nThey were carrying a chest that contains a small treasure horde. You will need to scare off the vulture before you can take the treasure.",
            "health_range": (1, 5),
            "power_range": (1, 3),
            "money_range": (1000, 1500)
        },
        {
            "name": "Stone Golem",
            "description": "A massive stone golem blocks your path. Its eyes glow faintly as it begins to move toward you.",
            "health_range": (100, 200),
            "power_range": (20, 40),
            "money_range": (0, 50)
        }
    ]

    monster = random.choice(monster_types)
    return {
        "name": monster["name"],
        "description": monster["description"],
        "health": random.randint(*monster["health_range"]),
        "power": random.randint(*monster["power_range"]),
        "money": random.randint(*monster["money_range"])
    }

# Demonstration of purchase_item()
print("Demonstrating purchase_item():")
num_purchased, leftover_money = purchase_item(123, 1000, 3)
print(f"Purchased: {num_purchased}, Remaining Money: {leftover_money}")

num_purchased, leftover_money = purchase_item(123, 201, 3)
print(f"Purchased: {num_purchased}, Remaining Money: {leftover_money}")

num_purchased, leftover_money = purchase_item(341, 2112)
print(f"Purchased: {num_purchased}, Remaining Money: {leftover_money}")

# Demonstration of new_random_monster
print("\nDemonstrating new_random_monster():")
for _ in range(3):
    monster = new_random_monster()
    print(f"Name: {monster['name']}")
    print(f"Description: {monster['description']}")
    print(f"Health: {monster['health']}, Power: {monster['power']}, Money: {monster['money']}\n")