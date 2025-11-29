# gamemap.py
import pygame

GRID_SIZE = 10
CELL_SIZE = 32
WINDOW_SIZE = GRID_SIZE * CELL_SIZE

def run_map(player_pos: tuple[int,int], monster_pos: tuple[int,int], town_pos: tuple[int,int]) -> tuple[str, tuple[int,int]]:
    """Runs the pygame map loop and returns action + new player position."""
    pygame.init()
    screen = pygame.display.set_mode((WINDOW_SIZE, WINDOW_SIZE))
    pygame.display.set_caption("Adventure Map")
    player_rect = pygame.Rect(player_pos[0]*CELL_SIZE, player_pos[1]*CELL_SIZE, CELL_SIZE, CELL_SIZE)
    clock = pygame.time.Clock(); running = True; action = "continue"
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT: running = False; action = "quit"
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP and player_rect.top > 0: player_rect.move_ip(0,-CELL_SIZE)
                elif event.key == pygame.K_DOWN and player_rect.bottom < WINDOW_SIZE: player_rect.move_ip(0,CELL_SIZE)
                elif event.key == pygame.K_LEFT and player_rect.left > 0: player_rect.move_ip(-CELL_SIZE,0)
                elif event.key == pygame.K_RIGHT and player_rect.right < WINDOW_SIZE: player_rect.move_ip(CELL_SIZE,0)
        screen.fill((0,0,0))
        for x in range(0,WINDOW_SIZE,CELL_SIZE):
            for y in range(0,WINDOW_SIZE,CELL_SIZE):
                pygame.draw.rect(screen,(50,50,50),(x,y,CELL_SIZE,CELL_SIZE),1)
        town_rect = pygame.Rect(town