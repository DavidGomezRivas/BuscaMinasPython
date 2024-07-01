import pygame
import sys
import random

# Inicialización de Pygame
pygame.init()

# Dimensiones de la pantalla
WIDTH, HEIGHT = 800, 600
ROWS, COLS = 10, 10
MINES = 20
CELL_SIZE = 40
GRID_OFFSET = (WIDTH - COLS * CELL_SIZE) // 2, (HEIGHT - ROWS * CELL_SIZE) // 2 + 40

# Colores
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (192, 192, 192)
DARK_GRAY = (160, 160, 160)
RED = (255, 0, 0)

# Fuente
FONT = pygame.font.SysFont('Arial', 24)

# Configuración de la pantalla
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Buscaminas")

class Minesweeper:
    def __init__(self):
        self.reset_game()

    def reset_game(self):
        self.grid = [[0 for _ in range(COLS)] for _ in range(ROWS)]
        self.mines = set()
        self.revealed = set()
        self.flags = set()
        self.game_over = False
        self.win = False
        self.place_mines()

    def place_mines(self):
        while len(self.mines) < MINES:
            row, col = random.randint(0, ROWS - 1), random.randint(0, COLS - 1)
            if (row, col) not in self.mines:
                self.mines.add((row, col))
                self.grid[row][col] = -1

        for row in range(ROWS):
            for col in range(COLS):
                if self.grid[row][col] == -1:
                    continue
                self.grid[row][col] = self.count_adjacent_mines(row, col)

    def count_adjacent_mines(self, row, col):
        count = 0
        for r in range(row - 1, row + 2):
            for c in range(col - 1, col + 2):
                if 0 <= r < ROWS and 0 <= c < COLS and (r, c) != (row, col):
                    if (r, c) in self.mines:
                        count += 1
        return count

    def reveal(self, row, col):
        if self.grid[row][col] == -1:
            self.game_over = True
            return
        self.revealed.add((row, col))
        if self.grid[row][col] == 0:
            for r in range(row - 1, row + 2):
                for c in range(col - 1, col + 2):
                    if 0 <= r < ROWS and 0 <= c < COLS and (r, c) != (row, col):
                        if (r, c) not in self.revealed:
                            self.reveal(r, c)
        if self.check_win():
            self.win = True

    def flag(self, row, col):
        if (row, col) in self.flags:
            self.flags.remove((row, col))
        else:
            self.flags.add((row, col))

    def check_win(self):
        return len(self.revealed) == ROWS * COLS - MINES

    def draw(self, screen):
        # Dibuja el mensaje de ganar o perder en la parte superior del tablero
        if self.game_over:
            self.draw_game_over(screen)
        elif self.win:
            self.draw_win(screen)

        for row in range(ROWS):
            for col in range(COLS):
                rect = pygame.Rect(GRID_OFFSET[0] + col * CELL_SIZE, GRID_OFFSET[1] + row * CELL_SIZE, CELL_SIZE, CELL_SIZE)
                if (row, col) in self.revealed:
                    if self.grid[row][col] == -1:
                        pygame.draw.rect(screen, RED, rect)
                    else:
                        pygame.draw.rect(screen, WHITE, rect)
                        if self.grid[row][col] > 0:
                            text = FONT.render(str(self.grid[row][col]), True, BLACK)
                            screen.blit(text, (rect.x + 15, rect.y + 10))
                else:
                    pygame.draw.rect(screen, GRAY, rect)
                    if (row, col) in self.flags:
                        pygame.draw.rect(screen, DARK_GRAY, rect)
                pygame.draw.rect(screen, BLACK, rect, 1)

    def draw_game_over(self, screen):
        text = FONT.render("Moriste! Pulsa R para reiniciar", True, BLACK)
        text_rect = text.get_rect(center=(WIDTH // 2, GRID_OFFSET[1] - 20))
        screen.blit(text, text_rect)

    def draw_win(self, screen):
        text = FONT.render("Ganaste! Pulsa R para reiniciar", True, BLACK)
        text_rect = text.get_rect(center=(WIDTH // 2, GRID_OFFSET[1] - 20))
        screen.blit(text, text_rect)

def draw_menu(screen):
    screen.fill(WHITE)
    title = FONT.render("Buscaminas", True, BLACK)
    play_button = FONT.render("Jugar", True, BLACK)
    instructions_button = FONT.render("Cómo Jugar", True, BLACK)
    exit_button = FONT.render("Salir", True, BLACK)
    
    screen.blit(title, (WIDTH // 2 - title.get_width() // 2, HEIGHT // 4))
    screen.blit(play_button, (WIDTH // 2 - play_button.get_width() // 2, HEIGHT // 2 - 50))
    screen.blit(instructions_button, (WIDTH // 2 - instructions_button.get_width() // 2, HEIGHT // 2))
    screen.blit(exit_button, (WIDTH // 2 - exit_button.get_width() // 2, HEIGHT // 2 + 50))

def draw_instructions(screen):
    screen.fill(WHITE)
    instructions = [
        "Cómo Jugar:",
        "1. Click izquierdo para revelar una celda.",
        "2. Click derecho para marcar/desmarcar una celda con una bandera.",
        "3. El objetivo es revelar todas las celdas que no tienen minas.",
        "4. Evita hacer clic en las minas.",
        "5. Ganas cuando todas las celdas sin minas son reveladas."
    ]
    y_offset = HEIGHT // 4
    for line in instructions:
        text = FONT.render(line, True, BLACK)
        screen.blit(text, (WIDTH // 2 - text.get_width() // 2, y_offset))
        y_offset += 40

    back_button = FONT.render("Volver", True, BLACK)
    screen.blit(back_button, (WIDTH // 2 - back_button.get_width() // 2, y_offset + 20))

def main():
    clock = pygame.time.Clock()
    game = Minesweeper()
    running = True
    state = "menu"

    while running:
        screen.fill(WHITE)

        if state == "menu":
            draw_menu(screen)
        elif state == "instructions":
            draw_instructions(screen)
        elif state == "game":
            game.draw(screen)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if state == "menu":
                if event.type == pygame.MOUSEBUTTONDOWN:
                    mx, my = pygame.mouse.get_pos()
                    if HEIGHT // 2 - 50 <= my <= HEIGHT // 2 - 50 + 30:
                        state = "game"
                    elif HEIGHT // 2 <= my <= HEIGHT // 2 + 30:
                        state = "instructions"
                    elif HEIGHT // 2 + 50 <= my <= HEIGHT // 2 + 80:
                        running = False
            elif state == "instructions":
                if event.type == pygame.MOUSEBUTTONDOWN:
                    state = "menu"
            elif state == "game":
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_r:
                        game.reset_game()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    mx, my = pygame.mouse.get_pos()
                    if GRID_OFFSET[0] <= mx < GRID_OFFSET[0] + COLS * CELL_SIZE and GRID_OFFSET[1] <= my < GRID_OFFSET[1] + ROWS * CELL_SIZE:
                        col = (mx - GRID_OFFSET[0]) // CELL_SIZE
                        row = (my - GRID_OFFSET[1]) // CELL_SIZE
                        if event.button == 1:  # Click izquierdo
                            game.reveal(row, col)
                        elif event.button == 3:  # Click derecho
                            game.flag(row, col)

        pygame.display.flip()
        clock.tick(30)

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
