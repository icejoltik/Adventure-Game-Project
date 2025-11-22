# game.py
# Bryan Strozyk
# 11/22/25
"""Main game script for interacting with RPG utility functions.

This script imports the gamefunctions module and runs a simple RPG loop
where the player can fight monsters, rest in town, buy items, equip weapons,
save progress, and quit the game.
"""

import gamefunctions

def main() -> None:
    """
    Runs the main game loop.

    The player begins with a set amount of HP and gold. During each loop,
    the player can choose to fight a monster, sleep to restore HP, shop for
    items, equip weapons, save progress, or quit. All gameplay logic is handled
    by functions in gamefunctions.py.

    Returns:
        None
    """
    filename = "savefile.json"
    load_choice = input("Load saved game? (y/n): ").strip().lower()
    if load_choice == "y":
        inventory, gold, equipped_weapon = gamefunctions.load_game(filename)
        hp = 30  # HP always resets
    else:
        hp = 30
        gold = 200
        inventory: list[dict] = []
        equipped_weapon: dict | None = None

    name = input("Enter your name, brave adventurer: ")
    gamefunctions.print_welcome(name, 40)

    while True:
        print("\nYou are in town.")
        print(f"Current HP: {hp}, Current Gold: {gold}")
        print("What would you like to do?")
        print("1) Leave town (Fight Monster)")
        print("2) Sleep (Restore HP for 5 Gold)")
        print("3) Shop (Buy Items)")
        print("4) Equip Weapon")
        print("5) Quit (without saving)")
        print("6) Save and Quit")

        choice = input("Enter choice: ").strip()

        if choice == "1":
            hp, gold = gamefunctions.fight_monster(hp, gold, inventory, equipped_weapon)
        elif choice == "2":
            hp, gold = gamefunctions.sleep(hp, gold)
        elif choice == "3":
            print("\nShop Menu:")
            print("1) Sword (50 gold)")
            print("2) Charm of Escape (75 gold)")
            shop_choice = input("Choose item: ").strip()
            if shop_choice == "1":
                inventory, gold = gamefunctions.purchase_item_from_shop(
                    gamefunctions.create_sword(), inventory, gold, 50)
            elif shop_choice == "2":
                inventory, gold = gamefunctions.purchase_item_from_shop(
                    gamefunctions.create_magic_charm(), inventory, gold, 75)
            else:
                print("Invalid shop choice.")
        elif choice == "4":
            equipped_weapon = gamefunctions.equip_item(inventory, "weapon")
        elif choice == "5":
            print("Farewell, adventurer!")
            break
        elif choice == "6":
            gamefunctions.save_game(filename, inventory, gold, equipped_weapon)
            print("Game saved. Goodbye!")
            break
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()
