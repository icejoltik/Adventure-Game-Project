# game.py
import random
import gamefunctions
from wanderingMonster import WanderingMonster
from gamemap import run_map

def main() -> None:
    filename = "savefile.json"
    town_square = (5, 5)

    # Load or start new game
    load_choice = input("Load saved game? (y/n): ").strip().lower()
    if load_choice == "y":
        inventory, gold, equipped_weapon, player_pos, monster_pos = gamefunctions.load_game(filename)
        monsters = [WanderingMonster("LoadedMonster", "A saved monster.", 20, 5, 50, "red", *monster_pos)]
    else:
        inventory = []
        gold = 200
        equipped_weapon = None
        player_pos = (0, 0)
        monsters = [
            WanderingMonster.create_random_monster(town_square),
            WanderingMonster.create_random_monster(town_square)
        ]

    hp = 30
    name = input("Enter your name, brave adventurer: ")
    gamefunctions.print_welcome(name, 40)

    move_counter = 0

    while True:
        print("\nYou are in town.")
        print(f"Current HP: {hp}, Gold: {gold}")
        print("1) Leave town (Explore Map)")
        print("2) Sleep (Restore HP for 5 Gold)")
        print("3) Shop")
        print("4) Equip Weapon")
        print("5) Quit (no save)")
        print("6) Save and Quit")

        choice = input("Enter choice: ").strip()

        if choice == "1":
            # Use first monster for map display
            monster_pos = (monsters[0].x, monsters[0].y) if monsters else (3, 3)
            action, player_pos = run_map(player_pos, monster_pos, town_square)

            if action == "town":
                continue
            elif action == "monster":
                for monster in monsters:
                    if (monster.x, monster.y) == player_pos:
                        print(f"You encounter a {monster.name}!")
                        print(monster.description)
                        hp, gold = gamefunctions.fight_monster(hp, gold, inventory, equipped_weapon)
                        if hp <= 0:
                            print("Game Over.")
                            return
                        monsters.remove(monster)

            # Move monsters every other turn
            move_counter += 1
            if move_counter % 2 == 0:
                for monster in monsters:
                    monster.move(random.choice(["up", "down", "left", "right"]), town_square)

            # Respawn if all defeated
            if not monsters:
                monsters = [
                    WanderingMonster.create_random_monster(town_square),
                    WanderingMonster.create_random_monster(town_square)
                ]

        elif choice == "2":
            hp, gold = gamefunctions.sleep(hp, gold)
        elif choice == "3":
            print("Shop:\n1) Sword (50 gold)\n2) Charm of Escape (75 gold)")
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
            monster_pos = (monsters[0].x, monsters[0].y) if monsters else (3, 3)
            gamefunctions.save_game(filename, inventory, gold, equipped_weapon, player_pos, monster_pos)
            print("Game saved. Goodbye!")
            break
        else:
            print("Invalid choice.")

if __name__ == "__main__":
    main()