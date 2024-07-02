import pygame
import sys
import os
import json

# Initialize Pygame
pygame.init()

# Screen dimensions
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('Profile')

# Colors
BLACK = (0, 0, 0)
DARK_BLUE = (0, 0, 50)
WHITE = (255, 255, 255)

# Load font with smaller size
font = pygame.font.Font(None, 36)

# File paths
username_file = 'username.txt'
scores_file = 'scores.json'

# Function to load username
def load_username():
    if os.path.exists(username_file):
        with open(username_file, 'r') as file:
            return file.read().strip()
    return "Guest"

# Function to load highest score
def load_highest_score():
    if os.path.exists(scores_file):
        with open(scores_file, 'r') as file:
            scores = json.load(file)
            return max(scores.values(), default=0)
    return 0

# Function to display text centered in a rectangle
def draw_text_centered(surface, text, color, rect):
    text_surface = font.render(text, True, color)
    text_rect = text_surface.get_rect(center=rect.center)
    surface.blit(text_surface, text_rect)

# Profile screen function
def profile_screen():
    running = True
    clock = pygame.time.Clock()

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    # Check if back button clicked
                    back_button_rect = pygame.Rect(20, 20, 100, 40)
                    if back_button_rect.collidepoint(event.pos):
                        print('Back button clicked. Returning to home...')
                        return  # Return to previous screen (assumed home page)

        screen.fill(DARK_BLUE)

        # Draw Profile title
        draw_text_centered(screen, 'Profile', WHITE, pygame.Rect(0, 50, SCREEN_WIDTH, 50))

        # Load username and highest score
        username = load_username()
        highest_score = load_highest_score()

        # Display username and highest score
        draw_text_centered(screen, f'Username: {username}', WHITE, pygame.Rect(300, 200, 200, 50))
        draw_text_centered(screen, f'Highest Score: {highest_score}', WHITE, pygame.Rect(300, 300, 200, 50))

        # Draw back button
        pygame.draw.rect(screen, WHITE, pygame.Rect(20, 20, 100, 40), 2)
        draw_text_centered(screen, 'Back', WHITE, pygame.Rect(20, 20, 100, 40))

        pygame.display.flip()
        clock.tick(30)

if __name__ == "__main__":
    profile_screen()
