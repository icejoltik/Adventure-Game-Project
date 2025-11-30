# gamemap.py
import pygame

GRID_SIZE = 10
CELL_SIZE = 32
WINDOW_SIZE = GRID_SIZE * CELL_SIZE

def run_map(player_pos: tuple[int, int], monster_pos: tuple[int, int], town_pos: tuple[int, int]) -> tuple[str, tuple[int, int]]:
    pygame.init()
    screen = pygame.display.set_mode((WINDOW_SIZE, WINDOW_SIZE))
    pygame.display.set_caption("Adventure Map")

    player_rect = pygame.Rect(player_pos[0] * CELL_SIZE, player_pos[1] * CELL_SIZE, CELL_SIZE, CELL_SIZE)
    town_rect = pygame.Rect(town_pos[0] * CELL_SIZE, town_pos[1] * CELL_SIZE, CELL_SIZE, CELL_SIZE)
    monster_rect = pygame.Rect(monster_pos[0] * CELL_SIZE, monster_pos[1] * CELL_SIZE, CELL_SIZE, CELL_SIZE)

    clock = pygame.time.Clock()
    running = True
    action = "continue"

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                action = "quit"
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP and player_rect.top > 0:
                    player_rect.move_ip(0, -CELL_SIZE)
                elif event.key == pygame.K_DOWN and player_rect.bottom < WINDOW_SIZE:
                    player_rect.move_ip(0, CELL_SIZE)
                elif event.key == pygame.K_LEFT and player_rect.left > 0:
                    player_rect.move_ip(-CELL_SIZE, 0)
                elif event.key == pygame.K_RIGHT and player_rect.right < WINDOW_SIZE:
                    player_rect.move_ip(CELL_SIZE, 0)

        screen.fill((0, 0, 0))

        for x in range(0, WINDOW_SIZE, CELL_SIZE):
            for y in range(0, WINDOW_SIZE, CELL_SIZE):
                pygame.draw.rect(screen, (50, 50, 50), (x, y, CELL_SIZE, CELL_SIZE), 1)

        pygame.draw.circle(screen, (0, 255, 0), town_rect.center, CELL_SIZE // 2)
        pygame.draw.circle(screen, (255, 0, 0), monster_rect.center, CELL_SIZE // 2)
        pygame.draw.rect(screen, (0, 0, 255), player_rect)

        pygame.display.flip()
        clock.tick(10)

        if player_rect.colliderect(town_rect):
            action = "town"
            running = False
        elif player_rect.colliderect(monster_rect):
            action = "monster"
            running = False

    pygame.quit()
    new_pos = (player_rect.x // CELL_SIZE, player_rect.y // CELL_SIZE)
    return action, new_pos