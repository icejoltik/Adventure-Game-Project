# wanderingMonster.py
import random

GRID_SIZE = 10

class WanderingMonster:
    """
    Represents a wandering monster on the game map.
    """

    def __init__(self, name: str, description: str, health: int, power: int,
                 gold: int, color: str, x: int, y: int) -> None:
        self.name = name
        self.description = description
        self.health = health
        self.power = power
        self.gold = gold
        self.color = color
        self.x = x
        self.y = y

    def move(self, direction: str, town_square: tuple[int, int]) -> None:
        """
        Attempts to move the monster in a given direction, staying within bounds
        and avoiding the town square.
        """
        new_x, new_y = self.x, self.y
        if direction == "up" and self.y > 0:
            new_y -= 1
        elif direction == "down" and self.y < GRID_SIZE - 1:
            new_y += 1
        elif direction == "left" and self.x > 0:
            new_x -= 1
        elif direction == "right" and self.x < GRID_SIZE - 1:
            new_x += 1

        if (new_x, new_y) != town_square:
            self.x, self.y = new_x, new_y

    @classmethod
    def create_random_monster(cls, town_square: tuple[int, int]) -> "WanderingMonster":
        """
        Creates a random monster with attributes and a random location.
        """
        monster_types = [
            {
                "name": "Zombie",
                "description": "A shambling zombie groans as it approaches.",
                "health_range": (20, 40),
                "power_range": (5, 10),
                "gold_range": (10, 50),
                "color": "red"
            },
            {
                "name": "Slime",
                "description": "A green slime jiggles menacingly.",
                "health_range": (10, 20),
                "power_range": (2, 6),
                "gold_range": (5, 20),
                "color": "green"
            },
            {
                "name": "Specter",
                "description": "A ghostly specter floats silently toward you.",
                "health_range": (15, 30),
                "power_range": (4, 8),
                "gold_range": (20, 60),
                "color": "blue"
            }
        ]

        monster = random.choice(monster_types)
        health = random.randint(*monster["health_range"])
        power = random.randint(*monster["power_range"])
        gold = random.randint(*monster["gold_range"])

        # Random location not equal to town square
        while True:
            x = random.randint(0, GRID_SIZE - 1)
            y = random.randint(0, GRID_SIZE - 1)
            if (x, y) != town_square:
                break

        return cls(monster["name"], monster["description"], health, power, gold,
                   monster["color"], x, y)
