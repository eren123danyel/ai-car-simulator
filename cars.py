import math
import time
import random
import pygame

def rotimage(img,topleft,rot):
    from main import screen
    rotimg = pygame.transform.rotate(img,rot)
    newrect = rotimg.get_rect(center=img.get_rect(topleft=topleft).center)
    return screen.blit(rotimg, newrect.topleft)

class AbstractCar:
    def __init__(self,maxvel,rotvel,imgs):
        self.lastcol = time.time()
        self.img = imgs[self.img_]
        self.maxvel = maxvel
        self.vel = 0
        self.rotvel = rotvel
        self.rot = 0 
        self.x = 230
        self.y = 330
        self.acc = 0.1
    
    def rotate(self, left=False,right=False):
        if left:
            self.rot += self.rotvel
        elif right:
            self.rot -= self.rotvel
    
    def draw(self):
        rotimage(self.img,(self.x,self.y),self.rot)
    
    def moveforward(self):
        # What's smaller the max vel or the current vel + acc
        self.vel = min(self.vel + self.acc, self.maxvel)
        self.move()
    
    def move(self):
        # calculate the direction using trigonometry
        rad = math.radians(self.rot)
        vert = math.cos(rad) * self.vel
        horz = math.sin(rad) * self.vel

        self.x -= horz
        self.y -= vert
    
    def slowdown(self):
        # Move the half of vel - acc until it's less than 0, then stop
        self.vel = max(self.vel - self.acc / 2,0)
        self.move()
    
    def collide(self,mask,mx=0,my=0):
        carmask = pygame.mask.from_surface(self.img)
        offset = (int(self.x-mx),int(self.y-my))
        hit = mask.overlap(carmask,offset)
        return hit

    def bounce(self):
        self.vel = -self.vel
        self.move()
    
    def movement(self,action):
        moved = False
        if action == 2:
            self.rotate(right=True)
        elif action == 1:
            self.rotate(left=True)
        elif action == 0:
            moved = True
            self.moveforward()
        if not moved:
            self.slowdown()

class PlayerCar(AbstractCar):
    def __init__(self, maxvel, rotvel, imgs):
        self.img_ = random.choice(["greencar","greycar","purplecar","redcar","whitecar"])
        super().__init__(maxvel, rotvel, imgs)
        

class Checkpoint():
    def __init__(self,img,posx,posy,idx,rot=0,changecolor=True,accessed=False):
        self.accessed = accessed
        self.img = img
        self.idx = idx
        self.posx = posx
        self.posy = posy
        self.rot = rot
        if rot != 0:
            self.rotimage(rot)
        self.changecolor = changecolor
        if changecolor:
            self.change_color((255,0,0))

    
    def rotimage(self,rot):
        rotimg = pygame.transform.rotate(self.img,rot)
        newrect = rotimg.get_rect(center=self.img.get_rect(topleft=(self.posx,self.posy)).center)
        self.img = rotimg
        self.posx,self.posy = newrect.topleft

    def change_color(self, new_color):
        # Create a temporary surface with the same size as the image
        temp_surface = pygame.Surface(self.img.get_size(), pygame.SRCALPHA)
        
        # Fill the temporary surface with the new color
        temp_surface.fill(new_color)
        
        # Blend the temporary surface with the original image using the multiply blending mode
        self.img = temp_surface

    def get_mask(self):
        return pygame.mask.from_surface(self.img)
    