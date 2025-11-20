#game.py
#Bryan Strozyk
#11/16/25

"""Main game script for interacting with RPG utility functions.

This script imports the gamefunctions module and runs a simple RPG loop
where the player can fight monsters, rest in town, or quit the game.
"""

import gamefunctions

def main() -> None:
    """
    Runs the main game loop.

    The player begins with a set amount of HP and gold. During each loop,
    the player can choose to fight a monster, sleep to restore HP, or quit.
    All gameplay logic is handled by functions in gamefunctions.py.

    Returns:
        None
    """
    # Initialize player stats
    hp: int = 30
    gold: int = 10
    name: str = input("Enter your name, brave adventurer: ")
    gamefunctions.print_welcome(name, 40)

    # Main game loop
    while True:
        print("\nYou are in town.")
        print(f"Current HP: {hp}, Current Gold: {gold}")
        print("What would you like to do?")
        print("1) Leave town (Fight Monster)")
        print("2) Sleep (Restore HP for 5 Gold)")
        print("3) Quit")

        choice: str = input("Enter choice: ").strip()

        if choice == "1":
            hp, gold = gamefunctions.fight_monster(hp, gold)
        elif choice == "2":
            hp, gold = gamefunctions.sleep(hp, gold)
        elif choice == "3":
            print("Farewell, adventurer!")
            break
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()