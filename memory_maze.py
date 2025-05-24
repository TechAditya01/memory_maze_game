import pygame
import random
import time

# Initialize
pygame.init()
WIDTH, HEIGHT = 600, 600
ROWS, COLS = 6, 6
CELL_SIZE = WIDTH // COLS
WHITE, BLACK, GREEN, RED, GRAY = (255,255,255), (0,0,0), (0,255,0), (255,0,0), (200, 200, 200)

win = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Memory Maze")

font = pygame.font.SysFont(None, 36)

# Generate random path
def generate_path():
    path = [(0,0)]
    x, y = 0, 0
    while (x, y) != (ROWS-1, COLS-1):
        if x < ROWS - 1 and y < COLS - 1:
            if random.choice([True, False]):
                x += 1
            else:
                y += 1
        elif x < ROWS - 1:
            x += 1
        else:
            y += 1
        path.append((x, y))
    return path

def draw_grid(path, show_path):
    for i in range(ROWS):
        for j in range(COLS):
            rect = pygame.Rect(j * CELL_SIZE, i * CELL_SIZE, CELL_SIZE, CELL_SIZE)
            if (i, j) in path and show_path:
                pygame.draw.rect(win, GREEN, rect)
            else:
                pygame.draw.rect(win, GRAY, rect)
            pygame.draw.rect(win, BLACK, rect, 2)

def show_message(text):
    overlay = pygame.Surface((WIDTH, HEIGHT))
    overlay.fill(WHITE)
    txt = font.render(text, True, BLACK)
    win.blit(overlay, (0,0))
    win.blit(txt, (WIDTH//2 - txt.get_width()//2, HEIGHT//2 - txt.get_height()//2))
    pygame.display.update()
    pygame.time.delay(2000)

def main():
    clock = pygame.time.Clock()
    run = True
    path = generate_path()
    show_path = True
    path_index = 0

    player_pos = (0, 0)

    draw_grid(path, show_path)
    pygame.display.update()
    pygame.time.delay(3000)
    show_path = False

    while run:
        clock.tick(60)
        win.fill(WHITE)
        draw_grid(path, show_path)
        pygame.draw.rect(win, RED, (player_pos[1]*CELL_SIZE, player_pos[0]*CELL_SIZE, CELL_SIZE, CELL_SIZE))
        pygame.display.update()

        x, y = player_pos
        new_pos = player_pos

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP and x > 0:
                    new_pos = (x - 1, y)
                elif event.key == pygame.K_DOWN and x < ROWS - 1:
                    new_pos = (x + 1, y)
                elif event.key == pygame.K_LEFT and y > 0:
                    new_pos = (x, y - 1)
                elif event.key == pygame.K_RIGHT and y < COLS - 1:
                    new_pos = (x, y + 1)

        if new_pos != player_pos:
            if path_index + 1 < len(path) and new_pos == path[path_index + 1]:
                path_index += 1
                player_pos = new_pos
            else:
                show_message("Wrong Move! Game Over.")
                run = False

        if player_pos == (ROWS-1, COLS-1):
            show_message("You Win!")
            run = False

    pygame.quit()


if __name__ == "__main__":
    main()
