# gamefunctions.py
import random
# Function to simulate purchasing an item
def purchase_item(item_price, starting_money, quantity_to_purchase=1):
 max_quantity = int(starting_money // item_price)
 quantity_purchased = min(quantity_to_purchase, max_quantity)
 remaining_money = starting_money - (quantity_purchased * item_price)
 return quantity_purchased, remaining_money
# Defines a function that creates a new random monster from the 3 below
def new_random_monster():
 monsters = {
 "Goblin": {
 "description": "This is a lone goblin. When it notices you deep in the
cavern, it rushes at you quickly with a shining dagger.",
 "health_range": (10, 30),
 "power_range": (5, 10),
 "money_range": (10, 50)
 },
 "Troll": {
 "description": "A menacing troll stands in your way, growling.",
 "health_range": (30, 60),
 "power_range": (10, 20),
 "money_range": (20, 100)
 },
 "Dragon": {
 "description": "A mighty dragon with scales that glisten in the
sunlight.",
 "health_range": (50, 100),
 "power_range": (20, 40),
 "money_range": (100, 500)
 }
 }
 #picks a key from the dictionaries
 monster_name = random.choice(list(monsters.keys()))
 monster_info = monsters[monster_name]

 monster = {
 "name": monster_name,
 "description": monster_info["description"],
 "health": round(random.uniform(*monster_info["health_range"]), 2),
 "power": round(random.uniform(*monster_info["power_range"]), 2),
 "money": round(random.uniform(*monster_info["money_range"]), 2)
 }

 return monster
# show functions with three different inputs
if __name__ == "__main__":
 # Demonstrate purchase_item function
 print("Test with default quantity_to_purchase:")
 print(purchase_item(50, 100)) # defaults to 1 item
 print("\nTest attempting to purchase more than can be afforded:")
 print(purchase_item(30, 50, 3)) # purchases 1 item
 print("\nTest with specific quantity_to_purchase:")
 print(purchase_item(10, 30, 2)) # purchases 2 items

 # use new_random_monster function
 print("\nNew random monsters:")
 print(new_random_monster()) # Ex 1
 print(new_random_monster()) # Ex 2
 print(new_random_monster()) # Ex 3