# gamefunctions.py
# Bryan Strozyk
# 11/29/25

import random
import json

def print_welcome(name: str, width: int) -> None:
    """Prints a centered welcome message for the given name."""
    message = f"Hello, {name}!"
    print(f"'{message.center(width)}'")

def print_shop_menu(item1Name: str, item1Price: float, item2Name: str, item2Price: float) -> None:
    """Prints a formatted shop menu with two items and their prices."""
    border = "/" + "-" * 22 + "\\"
    item1_line = "| {name:<12}{price:>8} |".format(name=item1Name, price=f"${item1Price:.2f}")
    item2_line = "| {name:<12}{price:>8} |".format(name=item2Name, price=f"${item2Price:.2f}")
    footer = "\\" + "-" * 22 + "/"
    print(border); print(item1_line); print(item2_line); print(footer)

def purchase_item(itemPrice: int, startingMoney: int, quantityToPurchase: int = 1) -> tuple[int, int]:
    """Calculates how many items can be purchased and returns quantity + remaining money."""
    max_affordable = startingMoney // itemPrice
    quantity_purchased = min(quantityToPurchase, max_affordable)
    money_remaining = startingMoney - (itemPrice * quantity_purchased)
    return quantity_purchased, money_remaining

def new_random_monster() -> dict[str, str | int]:
    """Generates a random monster with attributes drawn from predefined monster types."""
    monster_types = [
        {"name": "Goblin","description": "A lone goblin rushes at you.","health_range": (10, 30),"power_range": (5, 15),"money_range": (50, 150)},
        {"name": "Vulture","description": "A vulture guards treasure.","health_range": (1, 5),"power_range": (1, 3),"money_range": (1000, 1500)},
        {"name": "Stone Golem","description": "A massive stone golem blocks your path.","health_range": (100, 200),"power_range": (20, 40),"money_range": (0, 50)}
    ]
    monster = random.choice(monster_types)
    return {"name": monster["name"],"description": monster["description"],
            "health": random.randint(*monster["health_range"]),
            "power": random.randint(*monster["power_range"]),
            "money": random.randint(*monster["money_range"])}

# --- Inventory and Items ---
def create_sword() -> dict[str, str | int]:
    return {"name": "Sword","type": "weapon","maxDurability": 10,"currentDurability": 10,"damageBonus": 5}

def create_magic_charm() -> dict[str, str]:
    return {"name": "Charm of Escape","type": "consumable","effect": "Defeat monster instantly"}

def purchase_item_from_shop(item: dict, inventory: list[dict], gold: int, price: int) -> tuple[list[dict], int]:
    if gold >= price:
        inventory.append(item); gold -= price
        print(f"You purchased {item['name']}!")
    else: print("Not enough gold.")
    return inventory, gold

def equip_item(inventory: list[dict], item_type: str) -> dict | None:
    options = [item for item in inventory if item["type"] == item_type]
    if not options: print(f"No {item_type} items available."); return None
    print(f"Available {item_type}s:"); 
    for i, item in enumerate(options, start=1): print(f"{i}) {item['name']}")
    choice = input("Choose item: ").strip()
    if choice.isdigit():
        idx = int(choice) - 1
        if 0 <= idx < len(options): print(f"You equipped {options[idx]['name']}!"); return options[idx]
    print("No item equipped."); return None

def sleep(hp: int, gold: int) -> tuple[int, int]:
    if gold >= 5: hp += 10; gold -= 5; print("You feel rested. HP restored by 10.")
    else: print("Not enough gold to sleep!")
    return hp, gold

def fight_monster(hp: int, gold: int, inventory: list[dict], equipped_weapon: dict | None) -> tuple[int, int]:
    monster = new_random_monster(); monster_hp = monster["health"]
    print(f"\nA wild {monster['name']} appears!\n{monster['description']}")
    for item in inventory:
        if item["type"] == "consumable" and item["name"] == "Charm of Escape":
            print("Charm activates! Monster defeated instantly."); inventory.remove(item); gold += monster["money"]; return hp, gold
    while hp > 0 and monster_hp > 0:
        print(f"\nYour HP: {hp}, Monster HP: {monster_hp}\n1) Attack\n2) Run Away")
        action = input("Choose action: ").strip()
        if action == "1":
            player_damage = random.randint(5, 10)
            if equipped_weapon: player_damage += equipped_weapon["damageBonus"]; equipped_weapon["currentDurability"] -= 1
            monster_damage = random.randint(1, monster["power"])
            monster_hp -= player_damage; hp -= monster_damage
            print(f"You hit for {player_damage}! Monster hits for {monster_damage}!")
            if equipped_weapon and equipped_weapon["currentDurability"] <= 0: print(f"Your {equipped_weapon['name']} broke!"); inventory.remove(equipped_weapon); equipped_weapon = None
        elif action == "2": print("You ran away!"); break
        else: print("Invalid choice.")
    if hp <= 0: print("You have been defeated...")
    elif monster_hp <= 0: reward = monster["money"]; gold += reward; print(f"You defeated {monster['name']}! You gain {reward} gold.")
    return hp, gold

# --- Save/Load ---
def save_game(filename: str, inventory: list[dict], gold: int, equipped_weapon: dict | None, player_pos: tuple[int,int], monster_pos: tuple[int,int]) -> None:
    data = {"inventory": inventory,"gold": gold,"equipped_weapon": equipped_weapon,"player_pos": player_pos,"monster_pos": monster_pos}
    with open(filename, "w") as f: json.dump(data, f)
    print("Game saved.")

def load_game(filename: str) -> tuple[list[dict], int, dict | None, tuple[int,int], tuple[int,int]]:
    try:
        with open(filename, "r") as f: data = json.load(f)
        print("Game loaded.")
        return data["inventory"], data["gold"], data.get("equipped_weapon"), tuple(data.get("player_pos",(0,0))), tuple(data.get("monster_pos",(3,3)))
    except FileNotFoundError:
        print("No save found. Starting new game.")
        return [], 200, None, (0,0), (3,3)
