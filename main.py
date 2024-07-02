import pygame
import sys
import os
import json
from settings_screen import settings_screen
from tetris import game_board_page
from store_screen import store_screen
from profile_screen import profile_screen  # Import the profile screen function

# Initialize Pygame
pygame.init()
pygame.mixer.init()  # Initialize mixer for sound/music

# Screen dimensions
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('Tetrisorus')

# Colors
BLACK = (0, 0, 0)
DARK_BLUE = (0, 0, 50)
WHITE = (255, 255, 255)

# Load font with smaller size
font = pygame.font.Font(None, 24)

# Load logo image and resize
logo_image = pygame.image.load('assets/logo.png')
logo_image = pygame.transform.scale(logo_image, (220, 210))  # Resize to fit

# Load icon images and resize
icon_store = pygame.image.load('assets/store.png')
icon_store = pygame.transform.scale(icon_store, (74, 74))

icon_settings = pygame.image.load('assets/settings.png')
icon_settings = pygame.transform.scale(icon_settings, (67, 70))

icon_profile = pygame.image.load('assets/profile.png')
icon_profile = pygame.transform.scale(icon_profile, (55, 55))

# Load balance icon images and resize
icon_nuke = pygame.image.load('assets/balances/nuke.png')
icon_nuke = pygame.transform.scale(icon_nuke, (30, 30))

icon_bomb = pygame.image.load('assets/balances/bomb.png')
icon_bomb = pygame.transform.scale(icon_bomb, (30, 30))

icon_rewind = pygame.image.load('assets/balances/rewind.png')
icon_rewind = pygame.transform.scale(icon_rewind, (30, 30))

# File paths
username_file = 'username.txt'
balances_file = 'balances.json'
theme_music_file = 'assets/theme.mp3'  # Path to your theme music file

# Load balances from file
def load_balances():
    if os.path.exists(balances_file):
        with open(balances_file, 'r') as file:
            return json.load(file)
    else:
        # Create balances file with all balances set to 0
        balances = {'nukes': 0, 'bombs': 0, 'rewinds': 0}
        save_balances(balances)
        return balances

# Save balances to file
def save_balances(balances):
    with open(balances_file, 'w') as file:
        json.dump(balances, file)

# Function to display text centered in a rectangle
def draw_text_centered(surface, text, color, rect):
    text_surface = font.render(text, True, color)
    text_rect = text_surface.get_rect(center=rect.center)  # Use center attribute of rect directly
    surface.blit(text_surface, text_rect)

# Function to handle login and save username
def handle_login(username):
    if username.strip() == '':
        print('Username is required.')
    else:
        print('Continue button clicked, Username:', username)
        with open(username_file, 'w') as file:
            file.write(username)
        home_page()

# Function to display the home page
def home_page():
    balances = load_balances()
    running = True
    clock = pygame.time.Clock()

    # Play background music with fade-in effect
    pygame.mixer.music.load(theme_music_file)
    pygame.mixer.music.set_volume(0.05)
    pygame.mixer.music.fadeout(3)
    pygame.mixer.music.play(-1, start=0.0, fade_ms=4000)  # Fade in over 4 seconds

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    # Check if start game button clicked
                    start_button_rect = pygame.Rect(300, 300, 200, 50)
                    if start_button_rect.collidepoint(event.pos):
                        print('Start Game button clicked. Starting game...')
                        # Replace with logic to start the game
                        # Stop music before navigating to game board screen
                        pygame.mixer.music.stop()
                        game_board_page(
                            screen
                        )  # Assuming game_board_page() handles the game board
                    # Check if store icon clicked
                    icon_store_rect = pygame.Rect(280, 390, 74, 74)
                    if icon_store_rect.collidepoint(event.pos):
                        print('Store icon clicked. Redirecting to store...')
                        store_screen()  # Navigate to store screen
                    # Check if settings icon clicked
                    icon_settings_rect = pygame.Rect(370, 395, 67, 70)
                    if icon_settings_rect.collidepoint(event.pos):
                        print('Settings icon clicked. Redirecting to settings...')
                        settings_screen()  # Navigate to settings screen
                    icon_profile_rect = pygame.Rect(460, 400, 55, 55)
                    if icon_profile_rect.collidepoint(event.pos):
                        print('Profile icon clicked. Redirecting to profile...')
                        profile_screen()  # Navigate to profile page

        screen.fill(DARK_BLUE)

        # Draw Tetrisorus logo in the center
        logo_rect = logo_image.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 100))
        screen.blit(logo_image, logo_rect)

        # Draw Start Game button
        start_button_rect = pygame.Rect(300, 300, 200, 50)
        pygame.draw.rect(screen, WHITE, start_button_rect, 2)
        draw_text_centered(screen, 'Start Game', WHITE, start_button_rect)

        # Draw icons below the Start Game button
        screen.blit(icon_store, (280, 390))
        screen.blit(icon_settings, (370, 395))
        screen.blit(icon_profile, (460, 406))

        # Calculate starting x-position for balance icons to be centered
        total_icons_width = 3 * 30 + 2 * 50  # 3 icons, 2 gaps of 50px each
        start_x = (SCREEN_WIDTH - total_icons_width) // 2

        # Draw balance icons and quantities in the center
        screen.blit(icon_nuke, (start_x, 20))
        screen.blit(icon_bomb, (start_x + 80, 20))
        screen.blit(icon_rewind, (start_x + 160, 20))
        draw_text_centered(screen, f"{balances['nukes']}", WHITE,
                           pygame.Rect(start_x + 40, 20, 20, 30))
        draw_text_centered(screen, f"{balances['bombs']}", WHITE,
                           pygame.Rect(start_x + 120, 20, 20, 30))
        draw_text_centered(screen, f"{balances['rewinds']}", WHITE,
                           pygame.Rect(start_x + 200, 20, 20, 30))

        pygame.display.flip()
        clock.tick(30)

# Function to simulate the login page
def login_page():
    running = True
    clock = pygame.time.Clock()

    username = ''
    input_active = False
    input_rect = pygame.Rect(250, 350, 300, 40)  # Adjusted position for username input box
    continue_button_rect = pygame.Rect(300, 450, 200, 50)  # Adjusted position for continue button

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    # Check if username input box clicked
                    if input_rect.collidepoint(event.pos):
                        input_active = True
                    else:
                        input_active = False
                    # Check if continue button clicked
                    if continue_button_rect.collidepoint(event.pos):
                        handle_login(username)
            elif event.type == pygame.KEYDOWN:
                if input_active:
                    if event.key == pygame.K_BACKSPACE:
                        username = username[:-1]
                    else:
                        username += event.unicode

        screen.fill(DARK_BLUE)

        # Draw Tetrisorus logo above username input box
        logo_rect = logo_image.get_rect(center=(SCREEN_WIDTH // 2, 150))
        screen.blit(logo_image, logo_rect)

        # Draw text above username input box
        text_rect = pygame.Rect(200, 300, 400, 50)  # Adjusted position for text
        draw_text_centered(screen, 'Please type your username and press continue', WHITE, text_rect)

        # Draw username input box
        pygame.draw.rect(screen, WHITE, input_rect, 2)
        draw_text_centered(screen, username, WHITE, input_rect)

        # Draw continue button
        pygame.draw.rect(screen, WHITE, continue_button_rect, 2)
        draw_text_centered(screen, 'Continue', WHITE, continue_button_rect)

        pygame.display.flip()
        clock.tick(30)

if __name__ == "__main__":
    if os.path.exists(username_file):
        home_page()
    else:
        login_page()
