# npc.py
import pygame

class NPC:
    """
    Represents a non-player character (NPC) in town.
    Stores name, dialogue, position, and image/fallback color.
    """

    def __init__(self, name: str, dialogue: str, x: int, y: int, color=(200, 200, 0), image_path=None):
        self.name = name
        self.dialogue = dialogue
        self.x = x
        self.y = y
        self.color = color
        self.image_path = image_path
        self.image = None

    def load_image(self, size: tuple[int, int]) -> None:
        try:
            if self.image_path:
                img = pygame.image.load(self.image_path)
                self.image = pygame.transform.scale(img, size)
        except (pygame.error, FileNotFoundError):
            # fallback rectangle
            surf = pygame.Surface(size)
            surf.fill(self.color)
            self.image = surf

    def interact(self) -> str:
        """Return dialogue when player collides with NPC."""
        return f"{self.name} says: {self.dialogue}"
