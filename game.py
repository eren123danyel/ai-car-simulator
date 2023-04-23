import menu
from datetime import datetime
import time

def scale_img(img,scl):
    import main
    pygame = main.pygame
    # Scale image by multiplying height and width by the same value
    return pygame.transform.scale(img,(round(img.get_width()*scl),round(img.get_height()*scl)))


def load_imgs():
    # All assets from https://www.techwithtim.net/
    import pygame
    # Get all the cars
    greencar = scale_img(pygame.image.load("imgs/green-car.png"),0.5)
    greycar = scale_img(pygame.image.load("imgs/grey-car.png"),0.5)
    purplecar = scale_img(pygame.image.load("imgs/purple-car.png"),0.5)
    redcar = scale_img(pygame.image.load("imgs/red-car.png"),0.5)
    whitecar = scale_img(pygame.image.load("imgs/white-car.png"),0.5)

    finish = scale_img(pygame.image.load("imgs/finish.png"),0.8)
    # get a mask of the image for collision detection
    finishmask = pygame.mask.from_surface(finish)
    # Scale grass because it's too small
    grass = scale_img(pygame.image.load("imgs/grass.jpg"),2.1)
    trackborder = scale_img(pygame.image.load("imgs/track-border.png"),0.8)
    # get a mask of the image for collision detection
    trackbordermask = pygame.mask.from_surface(trackborder)
    # Scale track to be smaller
    track = scale_img(pygame.image.load("imgs/track.png"),0.8)
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


renderbool = True
renderbool2 = True
def game():
    global renderbool, renderbool2
    # Some ui elements (get drawn later)
    gobackbtn = menu.Button(780,620,100,50,"Go Back")
    savemodelbtn = menu.Button(780+100*1+10,620,100,50,"Save Model")
    renderbtn = menu.Button(780+100*2+10*2,620,100,50,"Render:    ")
    raysbtn = menu.Button(805+100*3+10*3,620,150,50,"Rays & Checks:    ")
    
    # If rendering is turned off
    if renderbtn.clicked():
        renderbool ^= True
        time.sleep(0.5)

    # If rendering of checkpoints and rays are off
    if raysbtn.clicked():
        renderbool2 ^= True
        time.sleep(0.5)

    import main
    # Train the model
    main.model.learn(total_timesteps=1, reset_num_timesteps=False)
    if renderbool:
        for idx, env in enumerate(main.env.envs):
            if idx == 0:
                env.render()
            else:
                env.onlycar()



    # Render some nice text
    menu.Text("AI Car Simulator",64).draw(720+280,50)
    
    # Render buttons 
    savemodelbtn.draw()
    gobackbtn.draw()
    renderbtn.draw()
    raysbtn.draw()
    

    if renderbool:
        menu.Text("On",16,(0,255,0)).draw((780+100*2+10*2+30,620))
    else:
        menu.Text("Off", 16,(255,0,0)).draw((780+100*2+10*2+30,620))

    if renderbool2:
        menu.Text("On",16,(0,255,0)).draw((805+100*3+10*3+55,620))
    else:
        menu.Text("Off", 16,(255,0,0)).draw((805+100*3+10*3+55,620))
        

    if savemodelbtn.clicked():
        main.model.save("models/air-car-model-"+datetime.now().strftime("%d-%m-%Y-%H-%M-%S"))

    if gobackbtn.clicked():
       menu.currentmenu = "Main Menu"