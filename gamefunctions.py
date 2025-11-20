# gamefunctions.py
# Bryan Strozyk
# 11/19/25

import random

def print_welcome(name: str, width: int) -> None:
    """
    Prints a centered welcome message for the given name.

    Args:
        name (str): The name to include in the welcome message.
        width (int): The total width of the output field.

    Returns:
        None
    """
    message = f"Hello, {name}!"
    print(f"'{message.center(width)}'")


def print_shop_menu(item1Name: str, item1Price: float, item2Name: str, item2Price: float) -> None:
    """
    Prints a formatted shop menu with two items and their prices.

    Args:
        item1Name (str): Name of the first item.
        item1Price (float): Price of the first item.
        item2Name (str): Name of the second item.
        item2Price (float): Price of the second item.

    Returns:
        None
    """
    border = "/" + "-" * 22 + "\\"
    item1_line = "| {name:<12}{price:>8} |".format(name=item1Name, price=f"${item1Price:.2f}")
    item2_line = "| {name:<12}{price:>8} |".format(name=item2Name, price=f"${item2Price:.2f}")
    footer = "\\" + "-" * 22 + "/"

    print(border)
    print(item1_line)
    print(item2_line)
    print(footer)


def purchase_item(itemPrice: int, startingMoney: int, quantityToPurchase: int = 1) -> tuple[int, int]:
    """
    Calculates how many items can be purchased given a starting amount of money,
    and returns both the quantity purchased and the remaining money.

    Args:
        itemPrice (int): The cost of a single item.
        startingMoney (int): The total amount of money available.
        quantityToPurchase (int, optional): Desired quantity to buy. Defaults to 1.

    Returns:
        tuple[int, int]: A pair (quantity_purchased, money_remaining).
    """
    max_affordable = startingMoney // itemPrice
    quantity_purchased = min(quantityToPurchase, max_affordable)
    money_remaining = startingMoney - (itemPrice * quantity_purchased)
    return quantity_purchased, money_remaining


def new_random_monster() -> dict[str, str | int]:
    """
    Generates a random monster with attributes drawn from predefined monster types.

    Returns:
        dict[str, str | int]: A dictionary containing the monster's attributes.
    """
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


# --- Inventory and Items ---

def create_sword() -> dict[str, str | int]:
    """Creates a sword item with durability and damage bonus."""
    return {
        "name": "Sword",
        "type": "weapon",
        "maxDurability": 10,
        "currentDurability": 10,
        "damageBonus": 5
    }


def create_magic_charm() -> dict[str, str]:
    """Creates a magic charm item that defeats a monster instantly."""
    return {
        "name": "Charm of Escape",
        "type": "consumable",
        "effect": "Defeat monster instantly"
    }


def purchase_item_from_shop(item: dict, inventory: list[dict], gold: int, price: int) -> tuple[list[dict], int]:
    """
    Purchases an item if the player has enough gold.

    Args:
        item (dict): The item to purchase.
        inventory (list[dict]): Current player inventory.
        gold (int): Current player gold.
        price (int): Price of the item.

    Returns:
        tuple[list[dict], int]: Updated inventory and gold.
    """
    if gold >= price:
        inventory.append(item)
        gold -= price
        print(f"You purchased {item['name']}!")
    else:
        print("Not enough gold to purchase this item.")
    return inventory, gold


def equip_item(inventory: list[dict], item_type: str) -> dict | None:
    """
    Allows the player to equip an item of a given type.

    Args:
        inventory (list[dict]): Current player inventory.
        item_type (str): Type of item to equip (e.g., 'weapon').

    Returns:
        dict | None: The equipped item, or None if none chosen.
    """
    options = [item for item in inventory if item["type"] == item_type]
    if not options:
        print(f"No {item_type} items available to equip.")
        return None

    print(f"Available {item_type}s:")
    for i, item in enumerate(options, start=1):
        print(f"{i}) {item['name']}")

    choice = input("Choose an item to equip (or press Enter to cancel): ").strip()
    if choice.isdigit():
        idx = int(choice) - 1
        if 0 <= idx < len(options):
            print(f"You equipped {options[idx]['name']}!")
            return options[idx]
    print("No item equipped.")
    return None


def sleep(hp: int, gold: int) -> tuple[int, int]:
    """Restores player HP in exchange for gold."""
    if gold >= 5:
        hp += 10
        gold -= 5
        print("You feel rested. HP restored by 10.")
    else:
        print("Not enough gold to sleep!")
    return hp, gold


def fight_monster(hp: int, gold: int, inventory: list[dict], equipped_weapon: dict | None) -> tuple[int, int]:
    """
    Handles a combat encounter between the player and a random monster.

    Args:
        hp (int): Current hit points of the player.
        gold (int): Current gold of the player.
        inventory (list[dict]): Player's inventory.
        equipped_weapon (dict | None): Currently equipped weapon.

    Returns:
        tuple[int, int]: Updated (hp, gold) after the combat encounter.
    """
    monster = new_random_monster()
    monster_hp = monster["health"]
    print(f"\nA wild {monster['name']} appears!")
    print(monster["description"])

    # Check for charm
    for item in inventory:
        if item["type"] == "consumable" and item["name"] == "Charm of Escape":
            print("Your Charm of Escape activates! The monster is defeated instantly.")
            inventory.remove(item)
            gold += monster["money"]
            return hp, gold

    while hp > 0 and monster_hp > 0:
        print(f"\nYour HP: {hp}, Monster HP: {monster_hp}")
        print("1) Attack")
        print("2) Run Away")
        action = input("Choose action: ").strip()

        if action == "1":
            # Base damage
            player_damage = random.randint(5, 10)
            # Weapon bonus
            if equipped_weapon:
                player_damage += equipped_weapon["damageBonus"]
                equipped_weapon["currentDurability"] -= 1
                if equipped_weapon["currentDurability"] <= 0:
                    print(f"Your {equipped_weapon['name']} broke!")
                    inventory.remove(equipped_weapon)
                    equipped_weapon = None

            monster_damage = random.randint(1, monster["power"])
            monster_hp -= player_damage
            hp -= monster_damage
            print(f"You hit the {monster['name']} for {player_damage} damage!")
            print(f"The {monster['name']} hits you for {monster_damage} damage!")
        elif action == "2":
            print("You ran away safely!")
            break
        else:
            print("Invalid choice. Try again.")

    if hp <= 0:
        print("You have been defeated...")
    elif monster_hp <= 0:
        reward = monster["money"]
        gold += reward
        print(f"You defeated the {monster['name']}! You