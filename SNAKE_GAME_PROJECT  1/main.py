import pygame
import random
import os

# Initialization of my pygame
pygame.init()

# Colors
White = (255, 255, 255)
W_Y_mix = (255, 250, 180)
Red = (255, 0, 0)
Purple = (128, 0, 128)
Black = (0, 0, 0)

# Game Screen dimensions
Game_width = 900
Game_height = 600

# Create a Game Window
GameWindow = pygame.display.set_mode((Game_width, Game_height))
pygame.display.set_caption("SNAKE GAME")

# paths of images and music
bg_img_path = os.path.join("assets", "images", "snake.jpg")
bg_music_path = os.path.join("assets", "music", "back.mp3")
gameover_music_path = os.path.join("assets", "music", "gameover.mp3")

# Load background image with the size of Game_width, Game_height
bgimg = pygame.image.load(bg_img_path)
bgimg = pygame.transform.scale(bgimg, (Game_width, Game_height)).convert_alpha()

# Load and play background music
pygame.mixer.music.load(bg_music_path)
pygame.mixer.music.play(-1)  # Loop music

# Clock and font
Clock = pygame.time.Clock()
Font = pygame.font.SysFont(None, 55)

# snake == ploat 
def plot_snake(window, color, snake_list, snake_size):
    for x, y in snake_list:
        pygame.draw.rect(window, color, [x, y, snake_size, snake_size])

# Display text
def screen_text(text, color, x, y):
    text_screen = Font.render(text,True,color)
    GameWindow.blit(text_screen, [x, y])

# Game Loop
def gameloop():
    snk_length = 1
    snk_list = []
    over_game = False
    exit_game = False

    Snake_x = 40   # Location of snake in X direction
    Snake_y = 60   # Location of snake in y direction
    Snake_size = 15    # Size of Snake and Food
    fps = 30
    velocity_x = 0
    velocity_y = 0
    Run_velocity = 5  # Running speed of Snake
    score = 0         # Starting Score 

    apple_x = random.randint(20, int(Game_width / 2))  # Food location using random 
    apple_y = random.randint(20, int(Game_height / 2))

    while not exit_game:

        if over_game:
            GameWindow.fill(W_Y_mix)                    # GameWindow filled by lite yellow and White color
            screen_text("GAME OVER! PRESS ENTER TO CONTINUE", Red, 50, 270)
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                    pygame.mixer.music.load(bg_music_path)
                    pygame.mixer.music.play(-1)
                    gameloop()
                if event.type == pygame.QUIT:            # Exit game 
                    exit_game = True

        else:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    exit_game = True

                if event.type == pygame.KEYDOWN:                            # Buttons Working 
                    if event.key == pygame.K_RIGHT and velocity_x != -Run_velocity:
                        velocity_x = Run_velocity
                        velocity_y = 0
                    elif event.key == pygame.K_LEFT and velocity_x != Run_velocity:
                        velocity_x = -Run_velocity
                        velocity_y = 0
                    elif event.key == pygame.K_UP and velocity_y != Run_velocity:
                        velocity_y = -Run_velocity
                        velocity_x = 0
                    elif event.key == pygame.K_DOWN and velocity_y != -Run_velocity:
                        velocity_y = Run_velocity
                        velocity_x = 0
                    elif event.key == pygame.K_c:
                        score += 10

            Snake_x += velocity_x     # Handle Snake Movement 
            Snake_y += velocity_y

            if abs(Snake_x - apple_x) < 20 and abs(Snake_y - apple_y) < 20:  # Food Zone 
                score += 10                                                  # Score each Apple 
                apple_x = random.randint(20, int(Game_width / 2))
                apple_y = random.randint(20, int(Game_height / 2))
                snk_length += 5                                              #  Adjust Snake Length as pr Apple 

            GameWindow.fill(White)
            GameWindow.blit(bgimg, (0, 0))
            screen_text("Score: " + str(score), Purple, 5, 5)                  # Show Score on Display
            plot_snake(GameWindow, Black, snk_list, Snake_size)

            head = [Snake_x, Snake_y]
            snk_list.append(head)

            if len(snk_list) > snk_length:
                del snk_list[0]

            pygame.draw.rect(GameWindow, Red, [apple_x, apple_y, Snake_size, Snake_size])          # Ploat Food 

            if (
                Snake_x < 0 or Snake_x > Game_width or                  #  Game Over if Snake Greater then Game Width and Height or Smaller then 0
                Snake_y < 0 or Snake_y > Game_height or
                head in snk_list[:-1]                                   # Game Over if touches it,self
            ):
                over_game = True
                pygame.mixer.music.load(gameover_music_path)            # load and play Game_over music 
                pygame.mixer.music.play()

        pygame.display.update()
        Clock.tick(fps)

# Start game
gameloop()
