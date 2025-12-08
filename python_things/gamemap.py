# gamemap.py
import pygame
from wanderingMonster import WanderingMonster
import random
import os

GRID_SIZE = 10
CELL_SIZE = 32
WINDOW_SIZE = GRID_SIZE * CELL_SIZE

def load_image(path: str, fallback_color: tuple[int, int, int], size: tuple[int, int]) -> pygame.Surface:
    """
    Attempts to load an image. If not found, returns a colored rectangle fallback.
    """
    try:
        image = pygame.image.load(path)
        image = pygame.transform.scale(image, size)
        return image
    except (pygame.error, FileNotFoundError):
        surface = pygame.Surface(size)
        surface.fill(fallback_color)
        return surface

def run_map(player_pos: tuple[int, int], monsters: list[WanderingMonster], town_pos: tuple[int, int]) -> tuple[str, tuple[int, int]]:
    """
    Runs the pygame map loop and returns action + new player position.
    """
    pygame.init()
    screen = pygame.display.set_mode((WINDOW_SIZE, WINDOW_SIZE))
    pygame.display.set_caption("Adventure Map")

    # Load images with fallbacks
    player_image = load_image("images/player.png", (0, 0, 0), (CELL_SIZE, CELL_SIZE))
    town_image   = load_image("images/town.png", (0, 255, 0), (CELL_SIZE, CELL_SIZE))
    monster_image = load_image("images/monster.png", (255, 0, 0), (CELL_SIZE, CELL_SIZE))

    player_rect = pygame.Rect(player_pos[0] * CELL_SIZE, player_pos[1] * CELL_SIZE, CELL_SIZE, CELL_SIZE)
    town_rect = pygame.Rect(town_pos[0] * CELL_SIZE, town_pos[1] * CELL_SIZE, CELL_SIZE, CELL_SIZE)

    clock = pygame.time.Clock()
    running = True
    action = "continue"
    player_moves = 0

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                action = "quit"
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP and player_rect.top > 0:
                    player_rect.move_ip(0, -CELL_SIZE)
                    player_moves += 1
                elif event.key == pygame.K_DOWN and player_rect.bottom < WINDOW_SIZE:
                    player_rect.move_ip(0, CELL_SIZE)
                    player_moves += 1
                elif event.key == pygame.K_LEFT and player_rect.left > 0:
                    player_rect.move_ip(-CELL_SIZE, 0)
                    player_moves += 1
                elif event.key == pygame.K_RIGHT and player_rect.right < WINDOW_SIZE:
                    player_rect.move_ip(CELL_SIZE, 0)
                    player_moves += 1
                elif event.key == pygame.K_ESCAPE:
                    action = "quit"
                    running = False

        # Monsters wander every other player move
        if player_moves > 0 and player_moves % 2 == 0:
            for monster in monsters:
                monster.move(random.choice(["up","down","left","right"]), town_pos)

        screen.fill((0, 0, 0))

        # ✅ Draw grid with lighter gray lines
        for x in range(0, WINDOW_SIZE, CELL_SIZE):
            for y in range(0, WINDOW_SIZE, CELL_SIZE):
                pygame.draw.rect(screen, (180, 180, 180), (x, y, CELL_SIZE, CELL_SIZE), 1)

        # Draw town
        screen.blit(town_image, town_rect.topleft)

        # Draw monsters
        for monster in monsters:
            monster_rect = pygame.Rect(monster.x * CELL_SIZE, monster.y * CELL_SIZE, CELL_SIZE, CELL_SIZE)
            screen.blit(monster_image, monster_rect.topleft)

        # Draw player
        screen.blit(player_image, player_rect.topleft)

        pygame.display.flip()
        clock.tick(10)

        # Auto-return when stepping on town
        if player_rect.colliderect(town_rect):
            action = "town"
            running = False

        # Check collisions with monsters
        for monster in monsters:
            monster_rect = pygame.Rect(monster.x * CELL_SIZE, monster.y * CELL_SIZE, CELL_SIZE, CELL_SIZE)
            if player_rect.colliderect(monster_rect):
                action = "monster"
                running = False

    pygame.quit()
    new_pos = (player_rect.x // CELL_SIZE, player_rect.y // CELL_SIZE)
    return action, new_pos
