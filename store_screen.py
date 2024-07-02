import pygame
import sys
from pygame.locals import *

# Initialize Pygame
pygame.init()

# Screen dimensions
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('Tetrisorus')

# Colors
DARK_BLUE = (0, 0, 50)
WHITE = (255, 255, 255)

# Load font with smaller size
font = pygame.font.Font(None, 24)

# Load icons for store and scale them
icon_rewind_ad = pygame.image.load('assets/store/rewind_ad.png')
icon_rewind_ad = pygame.transform.scale(icon_rewind_ad, (100, 124))

icon_rewind_10 = pygame.image.load('assets/store/rewind_buy_10.png')
icon_rewind_10 = pygame.transform.scale(icon_rewind_10, (100, 124))

icon_rewind_20 = pygame.image.load('assets/store/rewind_buy_20.png')
icon_rewind_20 = pygame.transform.scale(icon_rewind_20, (100, 124))

icon_bomb_ad = pygame.image.load('assets/store/bomb_ad.png')
icon_bomb_ad = pygame.transform.scale(icon_bomb_ad, (100, 124))

icon_bomb_10 = pygame.image.load('assets/store/bomb_buy_10.png')
icon_bomb_10 = pygame.transform.scale(icon_bomb_10, (100, 124))

icon_bomb_20 = pygame.image.load('assets/store/bomb_buy_20.png')
icon_bomb_20 = pygame.transform.scale(icon_bomb_20, (100, 124))

icon_nuke_ad = pygame.image.load('assets/store/nuke_ad.png')
icon_nuke_ad = pygame.transform.scale(icon_nuke_ad, (100, 124))

icon_nuke_10 = pygame.image.load('assets/store/nuke_buy_10.png')
icon_nuke_10 = pygame.transform.scale(icon_nuke_10, (100, 124))

icon_nuke_20 = pygame.image.load('assets/store/nuke_buy_20.png')
icon_nuke_20 = pygame.transform.scale(icon_nuke_20, (100, 124))

# Load store background image
store_bg = pygame.image.load('assets/store/store.png')
store_bg = pygame.transform.scale(store_bg, (164, 30))

# Function to display text centered in a rectangle
def draw_text_centered(surface, text, color, rect):
    text_surface = font.render(text, True, color)
    text_rect = text_surface.get_rect(center=rect.center)
    surface.blit(text_surface, text_rect)

# Function to handle events in store screen
def handle_events():
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()

# Function to display the store screen
def store_screen():
    running = True
    clock = pygame.time.Clock()

    # Calculate positions to center icons
    icon_width = 100
    total_width = 3 * icon_width + 4 * 50  # Total width of icons plus gaps
    start_x = (SCREEN_WIDTH - total_width) // 2

    rewind_y = 100
    bomb_y = 250
    nuke_y = 400

    while running:
        handle_events()

        screen.fill(DARK_BLUE)

        # Display store background image
        screen.blit(store_bg, (270, 50))

        # Display icons centered horizontally with some spacing
        screen.blit(icon_rewind_ad, (start_x, rewind_y))
        screen.blit(icon_rewind_10, (start_x + 150, rewind_y))
        screen.blit(icon_rewind_20, (start_x + 300, rewind_y))

        screen.blit(icon_bomb_ad, (start_x, bomb_y))
        screen.blit(icon_bomb_10, (start_x + 150, bomb_y))
        screen.blit(icon_bomb_20, (start_x + 300, bomb_y))

        screen.blit(icon_nuke_ad, (start_x, nuke_y))
        screen.blit(icon_nuke_10, (start_x + 150, nuke_y))
        screen.blit(icon_nuke_20, (start_x + 300, nuke_y))

        pygame.display.flip()
        clock.tick(30)

if __name__ == "__main__":
    store_screen()
