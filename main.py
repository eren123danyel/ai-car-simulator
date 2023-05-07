import pygame
import sys
from gymcar import AICarGame
from stable_baselines3 import DQN
from stable_baselines3.common.vec_env import DummyVecEnv
import time
from menu import menu


# Make an array for drawing graph
start_time = time.time()
x_axis = [0]
y_axis = [-10000]

# Game setup
pygame.init()
screen = pygame.display.set_mode((1280, 720),depth=16,flags=pygame.HWACCEL | pygame.HWSURFACE | pygame.DOUBLEBUF)
clock = pygame.time.Clock()


def scale_img(img,scl):
    # Scale image by multiplying height and width by the same value
    return pygame.transform.scale(img,(round(img.get_width()*scl),round(img.get_height()*scl)))

def load_imgs():
    # All assets from https://www.techwithtim.net/
    # Get all the cars
    greencar = scale_img(pygame.image.load("imgs/green-car.png"),0.5).convert_alpha()
    greycar = scale_img(pygame.image.load("imgs/grey-car.png"),0.5).convert_alpha()
    purplecar = scale_img(pygame.image.load("imgs/purple-car.png"),0.5).convert_alpha()
    redcar = scale_img(pygame.image.load("imgs/red-car.png"),0.5).convert_alpha()
    whitecar = scale_img(pygame.image.load("imgs/white-car.png"),0.5).convert_alpha()

    finish = scale_img(pygame.image.load("imgs/finish.png"),0.8).convert_alpha()
    # get a mask of the image for collision detection
    finishmask = pygame.mask.from_surface(finish)
    # Scale grass because it's too small
    grass = scale_img(pygame.image.load("imgs/grass.jpg"),2.1).convert_alpha()
    trackborder = scale_img(pygame.image.load("imgs/track-border.png"),0.8).convert_alpha()
    # get a mask of the image for collision detection
    trackbordermask = pygame.mask.from_surface(trackborder)
    # Scale track to be smaller
    track = scale_img(pygame.image.load("imgs/track.png"),0.8).convert_alpha()
    return {
        "greencar": greencar,
        "greycar": greycar,
        "purplecar": purplecar,
        "redcar": redcar,
        "whitecar": whitecar,
        "finish": finish,
        "finishmask": finishmask,
        "grass": grass,
        "trackborder": trackborder,
        "trackbordermask": trackbordermask,
        "track": track
    }

# Create and vectorize env 
env = DummyVecEnv([lambda: AICarGame(load_imgs()) for _ in range(10)])

# Set model
model = DQN("MlpPolicy", env, verbose=1)



# Set window properties
pygame.display.set_caption("AI Car")
icon = pygame.image.load('green-car.ico')
pygame.display.set_icon(icon)

def loop():
    # Check pygame events to see if the user pressed the X in the corner to close out
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
    
    # Fill the screen with a background color to remove anything rendered underneath
    screen.fill("white")

    # MENU
    menu()

    # Render on the screen
    pygame.display.flip()

    # Limits the screen to 30fps
    clock.tick(30)

if __name__ == "__main__":
    while True:
        loop()