"""Main game script for interacting with RPG utility functions.

This script imports the gamefunctions module and demonstrates its
functionality with user interaction.
"""

import gamefunctions

def main():
    name = input("Enter your name, brave adventurer: ")
    gamefunctions.print_welcome(name, 40)

    print("\nHere's what's in the shop today:")
    gamefunctions.print_shop_menu("Potion", 10.5, "Elixir", 25.0)

    print("\nLet's see what monster you'll face...")
    monster = gamefunctions.new_random_monster()
    print(f"Name: {monster['name']}")
    print(f"Description: {monster['description']}")
    print(f"Health: {monster['health']}, Power: {monster['power']}, Money: {monster['money']}")

    print("\nYou have 100 gold. Let's try buying an Elixir (25 gold each)...")
    qty, remaining = gamefunctions.purchase_item(25, 100, 2)
    print(f"Purchased: {qty}, Remaining Gold: {remaining}")

if __name__ == "__main__":
    main()