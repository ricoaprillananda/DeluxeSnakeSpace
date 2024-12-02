import pygame
import random

class SnakeGame:
    def __init__(self, width=1376, height=768):
        pygame.init()
        pygame.mixer.init()

        self.width = width
        self.height = height
        self.window = pygame.display.set_mode((self.width, self.height))  

        # Initialize Images
        self.food_image = pygame.image.load("assets/images/food.png")
        self.food_image = pygame.transform.scale(self.food_image, (30, 30))

        self.obstacle_image = pygame.image.load("assets/images/obstacle.png")
        self.obstacle_image = pygame.transform.scale(self.obstacle_image, (40, 40))

        self.background_space = pygame.image.load("assets/images/background_space.png")
        self.background_space = pygame.transform.scale(self.background_space, (self.width, self.height))

        self.background_jungle = pygame.image.load("assets/images/background_jungle.png")
        self.background_jungle = pygame.transform.scale(self.background_jungle, (self.width, self.height))

        self.power_image = pygame.image.load("assets/images/power.png")
        self.power_image = pygame.transform.scale(self.power_image, (25, 25))

        # Initialize Sounds
        self.background_music1 = pygame.mixer.Sound("assets/sounds/background_music_stage1.mp3")
        self.background_music2 = pygame.mixer.Sound("assets/sounds/background_music_stage2.mp3")
        self.win_music = pygame.mixer.Sound("assets/sounds/win_music.mp3")  
        self.eat_sound = pygame.mixer.Sound("assets/sounds/eat_sound.wav")
        self.power_sound = pygame.mixer.Sound("assets/sounds/power_sound.wav")
        self.rainbow_sound = pygame.mixer.Sound("assets/sounds/rainbow_mode_sound.wav")
        self.collision_sound = pygame.mixer.Sound("assets/sounds/collision_sound.wav")
        self.power_collision_sound = pygame.mixer.Sound("assets/sounds/power_collision_sound.wav") 

        # Game engine
        self.snake = [(100, 100)]
        self.food = self.generate_food()
        self.obstacles = []
        self.power = None
        self.power_active = False
        self.power_timer = 0
        self.direction = "RIGHT"
        self.lives = 3
        self.score = 0
        self.running = True
        self.clock = pygame.time.Clock()

        # Background and music
        self.current_background = self.background_space
        self.background_music1.play(-1)

    def generate_food(self):
        return (
            random.randint(0, (self.width - 30) // 30) * 30,
            random.randint(0, (self.height - 30) // 30) * 30,
        )

    def generate_power(self):
        return (
            random.randint(0, (self.width - 40) // 40) * 40,
            random.randint(0, (self.height - 40) // 40) * 40,
        )

    def generate_obstacle(self):
        return (
            random.randint(0, (self.width - 40) // 40) * 40,
            random.randint(0, (self.height - 40) // 40) * 40,
        )

    def start(self):
        while self.running:
            self.handle_events()
            self.update_snake()
            self.move_obstacles()
            self.render()

            if self.lives == 0:
                self.game_over()
                break

            if self.score == 20:
                self.change_stage()

            if self.score == 28:  
                self.game_won()

            self.clock.tick(15)

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP and self.direction != "DOWN":
                    self.direction = "UP"
                elif event.key == pygame.K_DOWN and self.direction != "UP":
                    self.direction = "DOWN"
                elif event.key == pygame.K_LEFT and self.direction != "RIGHT":
                    self.direction = "LEFT"
                elif event.key == pygame.K_RIGHT and self.direction != "LEFT":
                    self.direction = "RIGHT"

    def update_snake(self):
        head_x, head_y = self.snake[0]
        if self.direction == "UP":
            head_y -= 20  
        elif self.direction == "DOWN":
            head_y += 20  
        elif self.direction == "LEFT":
            head_x -= 20 
        elif self.direction == "RIGHT":
            head_x += 20  

        new_head = (head_x % self.width, head_y % self.height)
        self.snake = [new_head] + self.snake[:-1]

        # Food collision
        snake_rect = pygame.Rect(new_head[0], new_head[1], 20, 20)  
        food_rect = pygame.Rect(self.food[0], self.food[1], 30, 30)

        if snake_rect.colliderect(food_rect):
            self.snake.append(self.snake[-1])
            self.food = self.generate_food()
            self.score += 1
            self.eat_sound.play()

            if self.score % 2 == 0:
                self.obstacles.append(self.generate_obstacle())

            if self.score % 4 == 0:
                self.power = self.generate_power()

        # Power collision
        if self.power:
            power_rect = pygame.Rect(self.power[0], self.power[1], 40, 40)
            if snake_rect.colliderect(power_rect):
                self.power_active = True
                self.power_timer = pygame.time.get_ticks()
                self.rainbow_sound.play()
                self.power_sound.play()
                self.power = None

        # End power-up effect after 8 second
        if self.power_active and pygame.time.get_ticks() - self.power_timer > 8000:
            self.power_active = False
            self.rainbow_sound.stop()

        # Obstacle collision
        for obstacle in self.obstacles[:]:
            obstacle_rect = pygame.Rect(obstacle[0], obstacle[1], 40, 40)
            if snake_rect.colliderect(obstacle_rect):
                if self.power_active:
                    self.power_collision_sound.play() 
                    self.obstacles.remove(obstacle) 
                else:
                    self.collision_sound.play()  
                    self.lives -= 1
                    self.obstacles.remove(obstacle)

    def move_obstacles(self):
        for i in range(len(self.obstacles)):
            x, y = self.obstacles[i]
            x = (x + random.choice([-1, 1]) * 5) % self.width
            y = (y + random.choice([-1, 1]) * 5) % self.height
            self.obstacles[i] = (x, y)

    def draw_hexagon(self, center, color):
        x, y = center
        size = 10  
        points = [
            (x + size, y),
            (x + size // 2, y + size * 0.87),
            (x - size // 2, y + size * 0.87),
            (x - size, y),
            (x - size // 2, y - size * 0.87),
            (x + size // 2, y - size * 0.87),
        ]
        pygame.draw.polygon(self.window, color, points)

    def render(self):
        self.window.blit(self.current_background, (0, 0))

        # Initialize the snake
        for i, segment in enumerate(self.snake):
            if self.power_active:
                color = [random.choice([255, 0]) for _ in range(3)]
            elif self.score < 20:
                color = (255, 255, 255) 
            elif self.score < 28:
                color = (0, 128, 0)  
            elif self.score < 54:
                color = (0, 0, 255)  
            else:
                color = (128, 128, 128)  
            self.draw_hexagon(segment, color)

        # Food
        self.window.blit(self.food_image, self.food)

        # Power
        if self.power:
            self.window.blit(self.power_image, self.power)

        # obstacles
        for obstacle in self.obstacles:
            self.window.blit(self.obstacle_image, obstacle)

        # Lives and score
        font = pygame.font.SysFont("Arial", 24)
        lives_text = font.render(f"Lives: {self.lives}", True, (255, 255, 255))
        score_text = font.render(f"Score: {self.score}", True, (255, 255, 255))
        self.window.blit(lives_text, (10, 10))
        self.window.blit(score_text, (10, 40))

        pygame.display.flip()

    def change_stage(self):
        self.current_background = self.background_jungle
        self.background_music1.stop()
        self.background_music2.play(-1)

    def game_over(self):
        font = pygame.font.SysFont("Arial", 48)
        game_over_text = font.render("Game Over", True, (255, 0, 0))
        self.window.blit(game_over_text, (self.width // 2 - 150, self.height // 2 - 50))
        pygame.display.flip()
        pygame.time.wait(2000)
        self.running = False

    def game_won(self):
        font = pygame.font.SysFont("Arial", 48)
        win_text = font.render("You Win!", True, (0, 0, 0))
        self.window.blit(win_text, (self.width // 2 - 100, self.height // 2 - 50))
        pygame.display.flip()
        self.win_music.play()
        pygame.time.wait(3000)
        self.running = False

if __name__ == "__main__":
    game = SnakeGame()
    game.start()
