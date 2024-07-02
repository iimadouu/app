import pygame
import sys
import random
import json

# Screen dimensions
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

# Colors
BLACK = (0, 0, 0)
DARK_BLUE = (0, 0, 50)
WHITE = (255, 255, 255)
CYAN = (0, 255, 255)
BLUE = (0, 0, 255)
ORANGE = (255, 165, 0)
YELLOW = (255, 255, 0)
GREEN = (0, 255, 0)
PURPLE = (128, 0, 128)
RED = (255, 0, 0)

# Tetromino shapes (Tetris pieces)
tetrominoes = [
    [[1, 1, 1, 1]],                                # I-shape
    [[1, 1, 1],
     [0, 1, 0]],                                   # T-shape
    [[1, 1, 1],
     [1, 0, 0]],                                   # L-shape
    [[1, 1, 1],
     [0, 0, 1]],                                   # J-shape
    [[1, 1],
     [1, 1]],                                      # O-shape
    [[0, 1, 1],
     [1, 1, 0]],                                   # S-shape
    [[1, 1, 0],
     [0, 1, 1]]                                    # Z-shape
]

# Tetromino colors
tetromino_colors = [CYAN, PURPLE, ORANGE, BLUE, YELLOW, GREEN, RED]

# Grid dimensions and cell size
CELL_SIZE = 30
GRID_WIDTH = 10
GRID_HEIGHT = 20

# File paths
scores_file = 'scores.json'
balances_file = 'balances.json'

# Artifact images and positions
artifact_images = {
    'rewind': pygame.image.load('assets/artifacts/rewind.png'),
    'bomb': pygame.image.load('assets/artifacts/bomb.png'),
    'nuke': pygame.image.load('assets/artifacts/nuke.png')
}
artifact_positions = {
    'rewind': (SCREEN_WIDTH - 100, 100),
    'bomb': (SCREEN_WIDTH - 100, 200),
    'nuke': (SCREEN_WIDTH - 100, 300)
}

# Speed settings
BASE_FALL_SPEED = 500  # Milliseconds
score_thresholds = [1000, 10000, 50000]
speed_increases = [0.001, 0.002, 0.005]

def draw_piece(surface, piece, color, position):
    for y, row in enumerate(piece):
        for x, cell in enumerate(row):
            if cell == 1:
                pygame.draw.rect(surface, color,
                                 (position[0] + x * CELL_SIZE, position[1] + y * CELL_SIZE, CELL_SIZE, CELL_SIZE))
                pygame.draw.rect(surface, BLACK,
                                 (position[0] + x * CELL_SIZE, position[1] + y * CELL_SIZE, CELL_SIZE, CELL_SIZE), 1)

def draw_grid(surface, grid):
    for y in range(len(grid)):
        for x in range(len(grid[y])):
            if grid[y][x] != 0:
                pygame.draw.rect(surface, tetromino_colors[grid[y][x] - 1],
                                 (x * CELL_SIZE, y * CELL_SIZE, CELL_SIZE, CELL_SIZE))
                pygame.draw.rect(surface, BLACK,
                                 (x * CELL_SIZE, y * CELL_SIZE, CELL_SIZE, CELL_SIZE), 1)

def is_valid_move(piece, x, y, grid):
    for py, row in enumerate(piece):
        for px, cell in enumerate(row):
            if cell and (y + py >= GRID_HEIGHT or x + px < 0 or x + px >= GRID_WIDTH or grid[y + py][x + px]):
                return False
    return True

def place_piece(piece, x, y, grid, piece_index):
    for py, row in enumerate(piece):
        for px, cell in enumerate(row):
            if cell:
                grid[y + py][x + px] = piece_index + 1

def clear_rows(grid):
    rows_cleared = 0
    for y in range(GRID_HEIGHT):
        if all(grid[y]):
            rows_cleared += 1
            # Clear the row
            grid[y] = [0] * GRID_WIDTH
            # Move all rows above down by one
            for row in range(y, 0, -1):
                grid[row] = grid[row - 1][:]
            grid[0] = [0] * GRID_WIDTH
    return rows_cleared

def rotate_piece(piece):
    rotated_piece = [[piece[y][x] for y in range(len(piece))] for x in range(len(piece[0]) - 1, -1, -1)]
    return rotated_piece

def draw_text(surface, text, font, color, position):
    text_surface = font.render(text, True, color)
    surface.blit(text_surface, position)

def load_scores():
    try:
        with open(scores_file, 'r') as file:
            scores = json.load(file)
    except FileNotFoundError:
        # Create the file with default score (0)
        scores = {"default_score": 0}
        with open(scores_file, 'w') as file:
            json.dump(scores, file)
    return scores

def load_balances():
    try:
        with open(balances_file, 'r') as file:
            balances = json.load(file)
    except FileNotFoundError:
        # Create the file with default balances
        balances = {"nukes": 0, "bombs": 0, "rewinds": 0}
        with open(balances_file, 'w') as file:
            json.dump(balances, file)
    return balances

def save_balances(balances):
    with open(balances_file, 'w') as file:
        json.dump(balances, file, indent=4)

def save_scores(scores):
    with open(scores_file, 'w') as file:
        json.dump(scores, file, indent=4)

def use_bomb(grid):
    # Clear the last two rows completely
    del grid[-2:]
    grid.insert(0, [0] * GRID_WIDTH)
    grid.insert(0, [0] * GRID_WIDTH)

def use_nuke(grid):
    # Clear all tetrominos from the grid
    for row in range(GRID_HEIGHT):
        for col in range(GRID_WIDTH):
            grid[row][col] = 0

def update_speed(score):
    for i, threshold in enumerate(score_thresholds):
        if score >= threshold:
            return BASE_FALL_SPEED * (1 - speed_increases[i])
    return BASE_FALL_SPEED

def game_board_page(screen):
    running = True
    clock = pygame.time.Clock()

    # Initialize game variables
    grid = [[0] * GRID_WIDTH for _ in range(GRID_HEIGHT)]
    current_piece_index = random.randint(0, len(tetrominoes) - 1)
    current_piece = tetrominoes[current_piece_index]
    piece_color = tetromino_colors[current_piece_index]
    piece_x = GRID_WIDTH // 2 - len(current_piece[0]) // 2
    piece_y = 0
    game_over = False
    score = 0

    # Load scores and balances
    scores = load_scores()
    highest_score = scores.get('highest_score', 0)
    balances = load_balances()

    # Font for displaying score
    font = pygame.font.Font(None, 36)
    font_size_balances = pygame.font.Font(None, 22)

    # Falling speed variables
    FALL_SPEED = BASE_FALL_SPEED  # Initialize with base speed
    last_fall_time = pygame.time.get_ticks()

    # Load sound effect for line clear
    cleared_sound = pygame.mixer.Sound('assets/cleared.mp3')
    # Load sound effect for rotation
    rotate_sound = pygame.mixer.Sound('assets/rotate.mp3')

    # Variables for rewind functionality
    last_grid_state = None
    last_piece_x = None
    last_piece_y = None

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT and not game_over:
                    if is_valid_move(current_piece, piece_x - 1, piece_y, grid):
                        piece_x -= 1
                elif event.key == pygame.K_RIGHT and not game_over:
                    if is_valid_move(current_piece, piece_x + 1, piece_y, grid):
                        piece_x += 1
                elif event.key == pygame.K_DOWN and not game_over:
                    if is_valid_move(current_piece, piece_x, piece_y + 1, grid):
                        piece_y += 1
                elif event.key == pygame.K_UP and not game_over:
                    rotated_piece = rotate_piece(current_piece)
                    if is_valid_move(rotated_piece, piece_x, piece_y, grid):
                        current_piece = rotated_piece
                        # Play rotate sound effect
                        rotate_sound.play()
                    else:
                        # Adjust piece position if it's out of bounds after rotation
                        if piece_x < 0:
                            piece_x = 0
                        if piece_x + len(current_piece[0]) > GRID_WIDTH:
                            piece_x = GRID_WIDTH - len(current_piece[0])
                        if piece_y + len(current_piece) > GRID_HEIGHT:
                            piece_y = GRID_HEIGHT - len(current_piece)

                # Use artifact (Rewind) on key press 'R'
                elif event.key == pygame.K_r and not game_over:
                    if balances['rewinds'] >= 1:
                        # Save current state before placing piece
                        last_grid_state = [row[:] for row in grid]
                        last_piece_x = piece_x
                        last_piece_y = piece_y

                        # Deduct one from the rewind balance
                        balances['rewinds'] -= 1
                        save_balances(balances)

                        # Reset piece to top of board
                        piece_x = GRID_WIDTH // 2 - len(current_piece[0]) // 2
                        piece_y = 0

                # Use artifact (Bomb) on key press 'B'
                elif event.key == pygame.K_b and not game_over:
                    if balances['bombs'] >= 1:
                        # Use bomb artifact
                        use_bomb(grid)

                        # Deduct one from the bomb balance
                        balances['bombs'] -= 1
                        save_balances(balances)

                # Use artifact (Nuke) on key press 'N'
                elif event.key == pygame.K_n and not game_over:
                    if balances['nukes'] >= 1:
                        # Use nuke artifact
                        use_nuke(grid)

                        # Deduct one from the nuke balance
                        balances['nukes'] -= 1
                        save_balances(balances)

        # Update FALL_SPEED based on current score
        FALL_SPEED = update_speed(score)

        # Calculate elapsed time since last piece fall
        current_time = pygame.time.get_ticks()
        if current_time - last_fall_time > FALL_SPEED:
            # Update last fall time
            last_fall_time = current_time

            # Update game logic
            if not game_over:
                if not is_valid_move(current_piece, piece_x, piece_y + 1, grid):
                    place_piece(current_piece, piece_x, piece_y, grid, current_piece_index)
                    rows_cleared = clear_rows(grid)
                    if rows_cleared > 0:
                        # Play sound effect for each cleared row
                        cleared_sound.play()
                        score += (100 * rows_cleared)  # Example scoring: 100 points per cleared row
                    current_piece_index = random.randint(0, len(tetrominoes) - 1)
                    current_piece = tetrominoes[current_piece_index]
                    piece_x = GRID_WIDTH // 2 - len(current_piece[0]) // 2
                    piece_y = 0
                    piece_color = tetromino_colors[current_piece_index]

                    if not is_valid_move(current_piece, piece_x, piece_y, grid):
                        game_over = True
                else:
                    piece_y += 1

                # Update highest score if current score exceeds it
                if score > highest_score:
                    highest_score = score
                    scores['highest_score'] = highest_score
                    save_scores(scores)

        # Draw everything
        screen.fill(DARK_BLUE)

        # Draw game board
        draw_grid(screen, grid)

        # Draw current piece
        if current_piece is not None:
            draw_piece(screen, current_piece, piece_color, (piece_x * CELL_SIZE, piece_y * CELL_SIZE))

        # Draw artifacts and their quantities
        draw_text(screen, f"{balances['rewinds']}", font_size_balances, WHITE, (artifact_positions['rewind'][0] - 15, artifact_positions['rewind'][1]))
        draw_text(screen, f"{balances['bombs']}", font_size_balances, WHITE, (artifact_positions['bomb'][0] - 15, artifact_positions['bomb'][1]))
        draw_text(screen, f"{balances['nukes']}", font_size_balances, WHITE, (artifact_positions['nuke'][0] - 16, artifact_positions['nuke'][1]))

        screen.blit(artifact_images['rewind'], artifact_positions['rewind'])
        screen.blit(artifact_images['bomb'], artifact_positions['bomb'])
        screen.blit(artifact_images['nuke'], artifact_positions['nuke'])

        # Draw the score
        draw_text(screen, f"Score: {score}", font, WHITE, (SCREEN_WIDTH - 150, 20))

        # Draw the highest score
        draw_text(screen, f"Highest Score: {highest_score}", font, WHITE, (20, 20))

        pygame.display.flip()
        clock.tick(30)  # Limit frame rate to 30 FPS

if __name__ == "__main__":
    pygame.init()
    pygame.mixer.init()

    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption('Tetris')

    game_board_page(screen)
