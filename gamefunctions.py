# gamefunctions.py
# Bryan Strozyk
# 9/28/2025



import random


def print_welcome(name, width):
    """
    Prints a centered welcome message for the given name.

    Parameters:
    name (str): The name to include in the welcome message.
    width (int): The total width of the output field.

    Returns:
    None
    """
    message = f"Hello, {name}!"
    print(f"'{message.center(width)}'")


def print_shop_menu(item1Name, item1Price, item2Name, item2Price):
    """
    Prints a formatted shop menu with two items and their prices.

    Parameters:
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


def purchase_item(itemPrice, startingMoney, quantityToPurchase=1):
    """
    Calculates how many items can be purchased given a starting amount of money,
    and returns both the quantity purchased and the remaining money.

    Parameters:
        itemPrice (int): The cost of a single item.
        startingMoney (int): The total amount of money available.
        quantityToPurchase (int, optional): Desired quantity to buy. Defaults to 1 item.

    Returns:
        tuple: A pair (quantity_purchased, money_remaining), where:
            - quantity_purchased (int): The number of items successfully bought.
            - money_remaining (int): The amount of money left after the purchase.
    """	
    max_affordable = startingMoney // itemPrice
    quantity_purchased = min(quantityToPurchase, max_affordable)
    money_remaining = startingMoney - (itemPrice * quantity_purchased)
    return quantity_purchased, money_remaining

def new_random_monster():
    """
    Generates a random monster with attributes/characteristics drawn from the predefined monster types.

    Each monster has:
        - A name and description
        - Randomized health, power, and money values based on specific ranges based on type

    Returns:
        dict: A dictionary containing the monster's attributes:
            - 'name' (str): Monster type name
            - 'description' (str): Flavor describing the encounter
            - 'health' (int): Random health value within the monster's range
            - 'power' (int): Random power value within the monster's range
            - 'money' (int): Random money value within the monster's range
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


# Demonstration of print_welcome()
print("\nDemonstrating print_welcome():")
print_welcome("Jeff", 20)
print_welcome("Audrey", 30)
print_welcome("Bryannn", 25)

# Demonstration of print_shop_menu()
print("\nDemonstrating print_shop_menu():")
print_shop_menu("Apple", 31, "Pear", 1.234)
print_shop_menu("Egg", 0.23, "Bag of Oats", 12.34)
print_shop_menu("Sword", 99.99, "Shield", 75.5)