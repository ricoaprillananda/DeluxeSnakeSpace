import pygame
import sys
from game import SnakeGame  #

# Initialize Pygame
pygame.init()

def main():
    # Set up the display window and title
    screen_width = 1368
    screen_height = 768
    pygame.display.set_caption("Snake Game")
    
    # Initialize the game
    game = SnakeGame(width=screen_width, height=screen_height)
    
    # Start the game
    game.start()

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
