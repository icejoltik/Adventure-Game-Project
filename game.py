# game.py
"""Main game script for interacting with RPG utility functions."""

import random
import gamefunctions
from wanderingMonster import WanderingMonster

def main() -> None:
    hp = 30
    gold = 200
    inventory: list[dict] = []
    equipped_weapon: dict | None = None

    town_square = (5, 5)
    player_pos = (0, 0)

    # Start with two monsters
    monsters = [
        WanderingMonster.create_random_monster(town_square),
        WanderingMonster.create_random_monster(town_square)
    ]

    name = input("Enter your name, brave adventurer: ")
    gamefunctions.print_welcome(name, 40)

    while True:
        print("\nYou are in town.")
        print(f"Current HP: {hp}, Current Gold: {gold}")
        print("What would you like to do?")
        print("1) Leave town (Explore Map)")
        print("2) Sleep (Restore HP for 5 Gold)")
        print("3) Shop (Buy Items)")
        print("4) Equip Weapon")
        print("5) Quit (without saving)")
        print("6) Save and Quit")

        choice = input("Enter choice: ").strip()

        if choice == "1":
            # Example: every other move, monsters move
            for monster in monsters:
                monster.move(random.choice(["up","down","left","right"]), town_square)

            # Check collisions
            for monster in monsters:
                if (monster.x, monster.y) == player_pos:
                    print(f"You encounter a {monster.name}!")
                    hp, gold = gamefunctions.fight_monster(hp, gold, inventory, equipped_weapon)
                    if hp <= 0:
                        print("Game Over.")
                        return
                    monsters.remove(monster)
            if not monsters:
                monsters = [
                    WanderingMonster.create_random_monster(town_square),
                    WanderingMonster.create_random_monster(town_square)
                ]
        elif choice == "2":
            hp, gold = gamefunctions.sleep(hp, gold)
        elif choice == "3":
            print("\nShop Menu:\n1) Sword (50 gold)\n2) Charm of Escape (75 gold)")
            shop_choice = input("Choose item: ").strip()
            if shop_choice == "1":
                inventory, gold = gamefunctions.purchase_item_from_shop(gamefunctions.create_sword(), inventory, gold, 50)
            elif shop_choice == "2":
                inventory, gold = gamefunctions.purchase_item_from_shop(gamefunctions.create_magic_charm(), inventory, gold, 75)
        elif choice == "4":
            equipped_weapon = gamefunctions.equip_item(inventory, "weapon")
        elif choice == "5":
            print("Farewell, adventurer!")
            break
        elif choice == "6":
            gamefunctions.save_game("savefile.json", inventory, gold, equipped_weapon, player_pos, (monsters[0].x, monsters[0].y))
            print("Game saved. Goodbye!")
            break
        else:
            print("Invalid choice.")

if __name__ == "__main__":
    main()
