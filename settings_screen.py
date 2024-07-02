import pygame
import sys
import os

# Initialize Pygame
pygame.init()
pygame.mixer.init()  # Initialize mixer for sound/music

# Screen dimensions
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('Settings')

# Colors
BLACK = (0, 0, 0)
DARK_BLUE = (0, 0, 50)
WHITE = (255, 255, 255)

# Load font with smaller size
font = pygame.font.Font(None, 24)

# ToggleButton class for handling toggle functionality
class ToggleButton:
    def __init__(self, x, y, text):
        self.x = x
        self.y = y
        self.text = text
        self.state = False
        self.rect = pygame.Rect(x, y, 200, 30)
        self.font = pygame.font.Font(None, 24)
    
    def draw(self, surface):
        pygame.draw.rect(surface, WHITE, self.rect, 2)
        text_surface = self.font.render(self.text, True, WHITE)
        surface.blit(text_surface, (self.x + 10, self.y + 5))
        if self.state:
            pygame.draw.circle(surface, WHITE, (self.x + 170, self.y + 15), 7)
        else:
            pygame.draw.circle(surface, DARK_BLUE, (self.x + 170, self.y + 15), 7)
    
    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1 and self.rect.collidepoint(event.pos):
                self.state = not self.state
                if self.state:
                    # Perform action when toggled ON
                    if self.text == 'Disable Music:':
                        pygame.mixer.music.stop()
                    elif self.text == 'Disable Sound Effects:':
                        # Stop all sound effects
                        pygame.mixer.stop()
                        # Optionally stop specific sound effects like rotate.mp3, clear.mp3
                else:
                    # Perform action when toggled OFF
                    if self.text == 'Disable Music:':
                        pygame.mixer.music.play(-1)  # Resume music playback
                    # No need to resume sound effects, as they will play when triggered

# Function to display text centered in a rectangle
def draw_text_centered(surface, text, color, rect):
    text_surface = font.render(text, True, color)
    text_rect = text_surface.get_rect(center=rect.center)  # Use center attribute of rect directly
    surface.blit(text_surface, text_rect)

# Function to handle settings
def settings_screen():
    running = True
    clock = pygame.time.Clock()

    # Create ToggleButton for disabling music
    disable_music_button = ToggleButton(300, 200, 'Disable Music:')

    # Create ToggleButton for disabling sound effects
    disable_sound_effects_button = ToggleButton(300, 250, 'Sound Effects:')

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            # Handle events for toggle buttons
            disable_music_button.handle_event(event)
            disable_sound_effects_button.handle_event(event)

        screen.fill(DARK_BLUE)

        # Draw Settings title
        draw_text_centered(screen, 'Settings', WHITE, pygame.Rect(0, 50, SCREEN_WIDTH, 50))

        # Draw toggle buttons
        disable_music_button.draw(screen)
        disable_sound_effects_button.draw(screen)

        pygame.display.flip()
        clock.tick(30)

if __name__ == "__main__":
    settings_screen()
