import gym
from gym import spaces
import numpy as np
import cars
import time
import torch
import math

class AICarGame(gym.Env):
    def __init__(self,imgs):
        super().__init__()
        self.index = 0
        self.imgs = imgs
        # Define which moves the ai can do
        self.action_space = spaces.Discrete(3) # 0: move forward, 1: turn left, 2: turn right

        # get track information
        track_width, track_height = imgs["trackborder"].get_size()

        # Number of rays
        num_rays = 8
        self.ray_angles = np.linspace(0, 2*np.pi, num_rays)  # Spread rays over a 360-degree field of view
        max_range = 200
        self.max_range = max_range
        # Define the observation space with raycasts and position information
        low = np.zeros(num_rays + 4)  # All raycast distances start at 0, plus 4 extra values for positions
        high = np.concatenate((np.full(num_rays, max_range), [track_width, track_height, track_width, track_height]))  
        self.observation_space = spaces.Box(low=low, high=high, dtype=np.float32)

        # Checkpoints 
        from cars import Checkpoint
        self.checkpoints = [Checkpoint(self.imgs['finish'],209,309,1,0), Checkpoint(self.imgs['finish'],209,254,2,0), Checkpoint(self.imgs['finish'],206,167,3,0), Checkpoint(self.imgs['finish'],299,27,4,90), Checkpoint(self.imgs['finish'],421,27,5,90), Checkpoint(self.imgs['finish'],584,33,6,90), Checkpoint(self.imgs['finish'],622,175,7,0), Checkpoint(self.imgs['finish'],596,192,8,90), Checkpoint(self.imgs['finish'],478,199,9,90), Checkpoint(self.imgs['finish'],478,199,10,90), Checkpoint(self.imgs['finish'],412,198,11,90), Checkpoint(self.imgs['finish'],319,273,12,0), Checkpoint(self.imgs['finish'],403,283,13,90), Checkpoint(self.imgs['finish'],490,283,14,90), Checkpoint(self.imgs['finish'],592,285,15,90), Checkpoint(self.imgs['finish'],617,368,16,0), Checkpoint(self.imgs['finish'],619,452,17,0), Checkpoint(self.imgs['finish'],588,611,18,90), Checkpoint(self.imgs['finish'],498,592,19,0), Checkpoint(self.imgs['finish'],494,526,20,0), Checkpoint(self.imgs['finish'],490,481,21,0), Checkpoint(self.imgs['finish'],439,392,22,90), Checkpoint(self.imgs['finish'],439,392,23,90), Checkpoint(self.imgs['finish'],323,494,24,0), Checkpoint(self.imgs['finish'],327,564,25,0), Checkpoint(self.imgs['finish'],300,611,26,90), Checkpoint(self.imgs['finish'],205,610,27,0), Checkpoint(self.imgs['finish'],160,569,28,0), Checkpoint(self.imgs['finish'],109,515,29,0), Checkpoint(self.imgs['finish'],54,463,30,0), Checkpoint(self.imgs['finish'],22,380,31,0), Checkpoint(self.imgs['finish'],16,292,32,0), Checkpoint(self.imgs['finish'],9,197,33,0), Checkpoint(self.imgs['finish'],14,112,34,0), Checkpoint(self.imgs['finish'],99,29,35,90), Checkpoint(self.imgs['finish'],120,118,36,0), Checkpoint(self.imgs['finish'],119,188,37,0), Checkpoint(self.imgs['finish'],123,289,38,0), Checkpoint(self.imgs['finish'],619,555,39,0), Checkpoint(self.imgs['finish'],196,323,40,90,changecolor=False)]
        # For somereason i need to fix the position of the ones that are rotated
        for check in self.checkpoints:
            if check.rot == 90:
                check.posx = check.posx-30
                check.posy = check.posy+25

        # Start game 
        self.reset()

    def reset(self):
        self.player = cars.PlayerCar(4,4,self.imgs)
        # Set the inital values
        self.index = 0
        self.reward = 0
        self.done = False

        # Reset colors
        for i in range(0,len(self.checkpoints)-2):
            self.checkpoints[i].change_color((255,0,0))
        
        # get the intial state
        initial_state = self.get_extended_state()
        return initial_state

    def step(self, action):
        # Move car based on action
        self.player.movement(action)
        
        # Calculate speed penalty
        #speed_penalty = -0.0001 * abs(math.dist((self.cx,self.cy),(self.player.x,self.player.y))) * abs(self.player.maxvel - self.player.vel)
        speed_penalty =  0
        # Check if time since last collision with checkpoint is over 30seconds
        if time.time() > self.player.lastcol + 30:
            self.reward += -9999999 + speed_penalty
            self.done = True
        # if colliding with the track
        if self.player.collide(self.imgs["trackbordermask"]):
            self.reward += -9999999 + speed_penalty
            self.done = True

        # if colliding with a checkpoint
        elif self.player.collide(self.checkpoints[self.index].get_mask(),self.checkpoints[self.index].posx,self.checkpoints[self.index].posy):
            self.player.lastcol = time.time()
            if self.index == len(self.checkpoints) - 1:
                self.reward += 999999999999999999999999999999 + speed_penalty
                self.done = True
            else:
                self.reward += 9999999999 + speed_penalty
                self.done = False
            self.index += 1
        else:
            # Give a negative reward for not passing a checkpoint
            self.reward += speed_penalty
            self.done = False

        state = self.get_extended_state()

        return state,self.reward,self.done,{"speed penalty": speed_penalty}
    
    def render(self, mode="human"):
        import main
        import game
        screen = main.screen
        # Draw the imgs to screen
        screen.blit(self.imgs["grass"],(0,0))
        screen.blit(self.imgs["track"],(0,0))
        
        
        # Draw the checkpoints
        if game.renderbool2:
            for cp in self.checkpoints:
                # Draw the checkpoint as green if it's been passed
                if cp.idx == self.index:
                    cp.change_color((0,255,0))
                screen.blit(cp.img,(cp.posx,cp.posy))
        
        # Draw the border on top to hide the edges of the finish
        screen.blit(self.imgs["trackborder"],(0,0))
        
        # Draw rays if wanted
        if game.renderbool2:
            for angle in self.ray_angles:
                main.pygame.draw.line(screen, (0, 255, 0),
                                (self.player.x + self.player.img.get_width() // 2,
                                self.player.y + self.player.img.get_height() // 2),
                                self.raycast(angle), 3)
        
        # Draw the player
        self.player.draw()

    def onlycar(self):
        self.player.draw()


    def raycast(self, angle):
        ca = np.cos(angle)
        sa = np.sin(angle)

        startx = self.player.x + (self.player.img.get_width() // 2)
        starty = self.player.y + (self.player.img.get_height() // 2)

        endx = int(startx + (self.max_range * ca))
        endy = int(starty + (self.max_range * sa))
        
        step = self.max_range//100 if startx < endx else -(self.max_range//100)

        x = int(startx)
        y = int(starty)

        imgwidth = self.imgs['trackborder'].get_width()
        imgheight = self.imgs['trackborder'].get_height()

        # Bresenham algorithm
        while (x != endx) and (0 <= x < imgwidth) and (0 <= y < imgheight):
            if self.imgs['trackborder'].get_at((x, y)) != (255, 255, 255, 0):
                return x, y
            x += step
            y = int(starty + ((x - startx) * sa / ca))
        return endx, endy


    def get_extended_state(self):
        # Get the coords to the next checkpoint position
        cx, cy = self.checkpoints[self.index].img.get_rect().x, self.checkpoints[self.index].img.get_rect().y
        self.cx,self.cy = cx,cy
        # Raycast
        ray_distances = []
        for angle in self.ray_angles:
            ray_distance = abs(math.dist(self.raycast(angle),(self.player.x+self.player.img.get_rect().center[0],self.player.y+self.player.img.get_rect().center[1])))
            ray_distances.append(ray_distance)

        state = np.concatenate((np.array(ray_distances),np.array([self.player.x]),np.array([self.player.y]),np.array([cx]),np.array([cy])))    
        return torch.tensor(state, dtype=torch.float32)
