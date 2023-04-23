import pygame
import sys
from gymcar import AICarGame
from stable_baselines3 import DQN
from stable_baselines3.common.vec_env import DummyVecEnv



# Game setup
pygame.init()
screen = pygame.display.set_mode((1280, 720))
clock = pygame.time.Clock()
running = True


import game 

# Create and vectorize env 
env = DummyVecEnv([lambda: AICarGame(game.load_imgs()) for _ in range(20)])

# Set model
model = DQN("MlpPolicy", env, verbose=1)



# Set window properties
pygame.display.set_caption("AI Car")
icon = pygame.image.load('imgs/green-car.png')
pygame.display.set_icon(icon)

while running:
    # Check pygame events to see if the user pressed the X in the corner to close out
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            pygame.quit()
            sys.exit()
    
    # Fill the screen with a background color to remove anything rendered underneath
    screen.fill("white")

    # MENU
    import menu
    menu.menu()

    # Render on the screen
    pygame.display.flip()

    # Limits the screen to 30fps
    clock.tick(30)