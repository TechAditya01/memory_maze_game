import pygame
import random
import time
import os

# Initialize
pygame.init()
pygame.mixer.init()
WIDTH, HEIGHT = 600, 600
ROWS, COLS = 6, 6
CELL_SIZE = WIDTH // COLS
WHITE, BLACK, GREEN, RED, GRAY = (255,255,255), (0,0,0), (0,255,0), (255,0,0), (200, 200, 200)

win = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Memory Maze")

font = pygame.font.SysFont(None, 36)

# Load sounds (optional, handle missing files gracefully)
def load_sound(filename):
    try:
        return pygame.mixer.Sound(os.path.join(os.path.dirname(__file__), filename))
    except (pygame.error, FileNotFoundError):
        print(f"Warning: Sound file {filename} not found or could not be loaded.")
        return None

sound_win = load_sound("win.wav")
sound_lose = load_sound("lose.wav")

# High score file
HIGH_SCORE_FILE = "highscore.txt"

def load_high_score():
    if os.path.exists(HIGH_SCORE_FILE):
        with open(HIGH_SCORE_FILE, "r") as f:
            try:
                return int(f.read())
            except:
                return 0
    return 0

def save_high_score(score):
    with open(HIGH_SCORE_FILE, "w") as f:
        f.write(str(score))

# Generate random path
def generate_path(rows, cols):
    path = [(0,0)]
    x, y = 0, 0
    while (x, y) != (rows-1, cols-1):
        if x < rows - 1 and y < cols - 1:
            if random.choice([True, False]):
                x += 1
            else:
                y += 1
        elif x < rows - 1:
            x += 1
        else:
            y += 1
        path.append((x, y))
    return path

def draw_grid(path, show_path, rows, cols):
    for i in range(rows):
        for j in range(cols):
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

def draw_text(text, x, y, color=BLACK):
    txt = font.render(text, True, color)
    win.blit(txt, (x, y))

def main():
    global ROWS, COLS, CELL_SIZE
    clock = pygame.time.Clock()
    level = 1
    lives = 3
    high_score = load_high_score()

    while True:
        # Adjust difficulty by increasing grid size and decreasing path show time
        ROWS = COLS = min(6 + level - 1, 10)  # max 10x10 grid
        CELL_SIZE = WIDTH // COLS
        path = generate_path(ROWS, COLS)
        show_path = True
        path_index = 0
        player_pos = (0, 0)
        path_show_time = max(3000 - (level - 1) * 300, 1000)  # decrease show time per level, min 1 sec
        start_ticks = pygame.time.get_ticks()  # for countdown timer
        countdown_time = 30  # seconds for countdown timer

        run = True
        won = False
        correct_moves = 0  # count of correct moves in current run

        draw_grid(path, show_path, ROWS, COLS)
        pygame.display.update()
        pygame.time.delay(path_show_time)
        show_path = False

        while run:
            clock.tick(60)
            win.fill(WHITE)
            draw_grid(path, show_path, ROWS, COLS)
            pygame.draw.rect(win, RED, (player_pos[1]*CELL_SIZE, player_pos[0]*CELL_SIZE, CELL_SIZE, CELL_SIZE))

            # Draw lives, level, high score, countdown timer
            draw_text(f"Lives: {lives}", 10, 10)
            # draw_text(f"Level: {level}", 10, 40)
            draw_text(f"High Score: {high_score}", 10, 70)

            # Calculate countdown timer
            seconds_passed = (pygame.time.get_ticks() - start_ticks) / 1000
            time_left = max(0, countdown_time - seconds_passed)
            draw_text(f"Time Left: {int(time_left)}", WIDTH - 150, 10)

            # Draw current correct moves as score
            draw_text(f"Score: {correct_moves}", WIDTH - 150, 40)

            pygame.display.update()

            if time_left <= 0:
                lives -= 1
                if lives <= 0:
                    if sound_lose:
                        sound_lose.play()
                    show_message("Time's up! Game Over.")
                    pygame.quit()
                    return
                else:
                    show_message("Time's up! Try again.")
                    run = False
                    break

            x, y = player_pos
            new_pos = player_pos

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    return
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
                    correct_moves += 1
                    if correct_moves > high_score:
                        high_score = correct_moves
                        save_high_score(high_score)
                else:
                    lives -= 1
                    if lives <= 0:
                        if sound_lose:
                            sound_lose.play()
                        show_message("Wrong Move! Game Over.")
                        pygame.quit()
                        return
                    else:
                        show_message(f"Wrong Move! Lives left: {lives}")
                        run = False

            if player_pos == (ROWS-1, COLS-1):
                if sound_win:
                    sound_win.play()
                show_message("You Win!")
                won = True
                run = False

        if won:
            # level += 1
            # score = level - 1
            # if score > high_score:
            #     high_score = score
            #     save_high_score(high_score)
            pass
        else:
            # Reset level on game over
            # level = 1
            pass

        # Small delay before next level or retry
        pygame.time.delay(1000)

if __name__ == "__main__":
    main()
