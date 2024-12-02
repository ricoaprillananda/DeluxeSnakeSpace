import pygame
import sys
from game import SnakeGame  

class UI:
    def __init__(self):
        pygame.init()
        self.screen_width = 800
        self.screen_height = 600
        self.window = pygame.display.set_mode((self.screen_width, self.screen_height))
        pygame.display.set_caption("Snake Game")

        # Load fonts
        self.font = pygame.font.Font(None, 36)  
        self.big_font = pygame.font.Font(None, 72) 

        # Colors
        self.bg_color = (0, 0, 0)  
        self.text_color = (255, 255, 255)  

    def display_text(self, text, font, color, x, y):
        """Helper function to display text at given position"""
        text_surface = font.render(text, True, color)
        text_rect = text_surface.get_rect(center=(x, y))
        self.window.blit(text_surface, text_rect)

    def main_menu(self):
        """Displays the main menu where user can start or quit the game"""
        self.window.fill(self.bg_color)
        self.display_text("Welcome to Snake Game!", self.big_font, self.text_color, self.screen_width // 2, 150)
        self.display_text("Press SPACE to Start", self.font, self.text_color, self.screen_width // 2, 250)
        self.display_text("Press ESC to Quit", self.font, self.text_color, self.screen_width // 2, 350)

        pygame.display.update()

        # Wait for user input to start or quit the game
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:  
                        running = False
                    if event.key == pygame.K_ESCAPE:  #
                        pygame.quit()
                        sys.exit()

    def game_over(self, score):
        """Displays the game over screen with final score"""
        self.window.fill(self.bg_color)
        self.display_text("Game Over!", self.big_font, self.text_color, self.screen_width // 2, 150)
        self.display_text(f"Score: {score}", self.font, self.text_color, self.screen_width // 2, 250)
        self.display_text("Press SPACE to Restart", self.font, self.text_color, self.screen_width // 2, 350)
        self.display_text("Press ESC to Quit", self.font, self.text_color, self.screen_width // 2, 450)

        pygame.display.update()

        # Wait for user input to restart or quit the game
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:  
                        running = False
                    if event.key == pygame.K_ESCAPE:
                        pygame.quit()
                        sys.exit()

    def display_score(self, score):
        """Displays the current score at the top of the screen"""
        score_text = f"Score: {score}"
        self.display_text(score_text, self.font, self.text_color, self.screen_width // 2, 20)

    def update_screen(self, game, score):
        """Updates the screen during the game loop"""
        self.window.fill(self.bg_color)  
        game.render()  
        self.display_score(score)  
        pygame.display.update() 

# Main entry for UI-driven game loop
def run_game():
    ui = UI()
    game = SnakeGame(width=ui.screen_width, height=ui.screen_height)
    
    # Show the main menu
    ui.main_menu()

    # Start the game
    score = 0
    while True:
        game_running = True
        while game_running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
            
            game.update_snake()  
            score = len(game.snake) - 3  
            ui.update_screen(game, score)  

            if not game.running:  
                ui.game_over(score) 
                game = SnakeGame(width=ui.screen_width, height=ui.screen_height) 
                ui.main_menu()  

if __name__ == "__main__":
    run_game()
