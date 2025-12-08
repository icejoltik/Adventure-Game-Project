# gamemap.py
import pygame
from wanderingMonster import WanderingMonster
from npc import NPC
import random

GRID_SIZE = 10
CELL_SIZE = 32
WINDOW_SIZE = GRID_SIZE * CELL_SIZE

def load_image(path: str, fallback_color: tuple[int, int, int], size: tuple[int, int]) -> pygame.Surface:
    try:
        image = pygame.image.load(path)
        image = pygame.transform.scale(image, size)
        return image
    except (pygame.error, FileNotFoundError):
        surface = pygame.Surface(size)
        surface.fill(fallback_color)
        return surface

def wrap_text(text: str, font: pygame.font.Font, max_width: int) -> list[str]:
    words = text.split()
    lines = []
    current = []

    for word in words:
        test_line = " ".join(current + [word])
        if font.size(test_line)[0] <= max_width:
            current.append(word)
        else:
            if current:
                lines.append(" ".join(current))
            current = [word]

    if current:
        lines.append(" ".join(current))
    return lines

def draw_dialogue(screen: pygame.Surface, text: str, window_width: int, window_height: int,
                  font_size: int = 22, padding: int = 10, margin_bottom: int = 8,
                  bg_color=(0, 0, 0), text_color=(255, 255, 255), alpha: int = 200) -> None:
    font = pygame.font.Font(None, font_size)
    max_text_width = window_width - padding * 2
    lines = wrap_text(text, font, max_text_width)
    line_height = font.get_linesize()
    box_height = padding * 2 + line_height * len(lines)

    box_surface = pygame.Surface((window_width, box_height), pygame.SRCALPHA)
    box_surface.fill((*bg_color, alpha))
    box_top = window_height - box_height - margin_bottom
    screen.blit(box_surface, (0, box_top))

    y = box_top + padding
    for line in lines:
        text_surface = font.render(line, True, text_color)
        screen.blit(text_surface, (padding, y))
        y += line_height

def run_map(player_pos: tuple[int, int], monsters: list[WanderingMonster], town_pos: tuple[int, int]) -> tuple[str, tuple[int, int]]:
    pygame.init()
    screen = pygame.display.set_mode((WINDOW_SIZE, WINDOW_SIZE))
    pygame.display.set_caption("Adventure Map")

    player_image = load_image("images/player.png", (0, 0, 0), (CELL_SIZE, CELL_SIZE))
    town_image = load_image("images/town.png", (0, 255, 0), (CELL_SIZE, CELL_SIZE))
    monster_image = load_image("images/monster.png", (255, 0, 0), (CELL_SIZE, CELL_SIZE))

    npc_list = [
        NPC("Old Sage", "Beware the monsters beyond the town!", 4, 5, image_path="images/npc_sage.png"),
        NPC("Merchant", "I sell rare goods in the shop. Come visit!", 6, 5, image_path="images/npc_merchant.png")
    ]
    for npc in npc_list:
        npc.load_image((CELL_SIZE, CELL_SIZE))

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

        if player_moves > 0 and player_moves % 2 == 0:
            for monster in monsters:
                monster.move(random.choice(["up", "down", "left", "right"]), town_pos)

        screen.fill((0, 0, 0))

        # Lighter grid lines
        for x in range(0, WINDOW_SIZE, CELL_SIZE):
            for y in range(0, WINDOW_SIZE, CELL_SIZE):
                pygame.draw.rect(screen, (180, 180, 180), (x, y, CELL_SIZE, CELL_SIZE), 1)

        screen.blit(town_image, town_rect.topleft)

        for monster in monsters:
            monster_rect = pygame.Rect(monster.x * CELL_SIZE, monster.y * CELL_SIZE, CELL_SIZE, CELL_SIZE)
            screen.blit(monster_image, monster_rect.topleft)

        for npc in npc_list:
            npc_rect = pygame.Rect(npc.x * CELL_SIZE, npc.y * CELL_SIZE, CELL_SIZE, CELL_SIZE)
            screen.blit(npc.image, npc_rect.topleft)

        screen.blit(player_image, player_rect.topleft)

        pygame.display.flip()
        clock.tick(10)

        if player_rect.colliderect(town_rect):
            action = "town"
            running = False

        for monster in monsters:
            monster_rect = pygame.Rect(monster.x * CELL_SIZE, monster.y * CELL_SIZE, CELL_SIZE, CELL_SIZE)
            if player_rect.colliderect(monster_rect):
                action = "monster"
                running = False

        for npc in npc_list:
            npc_rect = pygame.Rect(npc.x * CELL_SIZE, npc.y * CELL_SIZE, CELL_SIZE, CELL_SIZE)
            if player_rect.colliderect(npc_rect):
                draw_dialogue(screen, npc.interact(), WINDOW_SIZE, WINDOW_SIZE)
                pygame.display.flip()
                pygame.time.delay(1500)

    pygame.quit()
    new_pos = (player_rect.x // CELL_SIZE, player_rect.y // CELL_SIZE)
    return action, new_pos

