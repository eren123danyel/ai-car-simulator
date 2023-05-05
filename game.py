import menu
from datetime import datetime
import time
import matplotlib as mpl
import matplotlib.pyplot as plt
import matplotlib.backends.backend_agg as agg
import numpy as np

def scale_img(img,scl):
    import main
    pygame = main.pygame
    # Scale image by multiplying height and width by the same value
    return pygame.transform.scale(img,(round(img.get_width()*scl),round(img.get_height()*scl)))



def draw_graph(x,y):
    mpl.use('Agg')
    width, height = 550,400
    dpi = 100
    fig, ax = plt.subplots(figsize=(width / dpi, height/dpi),dpi=dpi)
    x = np.array(x)
    y = np.array(y)
    # Add axis data and title and legend
    ax.set_title("Graph of max reward since start of program")
    ax.set_xlabel("Time since start of program (Seconds)")
    ax.set_ylabel("Max reward")
    # Plot data
    ax.plot(x,y)
    
    try:
        # Draw best fit line
        z = np.polyfit(x, y, 1)
        p = np.poly1d(z)

        # Add trendline to plot
        ax.plot(x,p(x))
        # Determine legend
        ax.legend(["Real data","Best fit"],loc="lower right")
    except:
        pass
    

    canvas = agg.FigureCanvasAgg(fig)
    canvas.draw()
    renderer = canvas.get_renderer()
    raw_data = renderer.tostring_rgb()
    import main
    surf = main.pygame.image.fromstring(raw_data, (width,height), "RGB")
    return surf



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
    gobackbtn = menu.Button(780+25,620,100,50,"Go Back")
    savemodelbtn = menu.Button(780+100*1+10+25,620,100,50,"Save Model")
    renderbtn = menu.Button(780+100*2+10*2+25,620,100,50,"Render:    ")
    raysbtn = menu.Button(805+100*3+10*3+25,620,150,50,"Rays & Checks:    ")
    
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
        menu.Text("On",16,(0,255,0)).draw((780+100*2+10*2+30+25,620))
    else:
        menu.Text("Off", 16,(255,0,0)).draw((780+100*2+10*2+30+25,620))

    if renderbool2:
        menu.Text("On",16,(0,255,0)).draw((805+100*3+10*3+55+25,620))
    else:
        menu.Text("Off", 16,(255,0,0)).draw((805+100*3+10*3+55+25,620))
        

    if savemodelbtn.clicked():
        # Save the current model with the date and time
        main.model.save("models/air-car-model-"+datetime.now().strftime("%d-%m-%Y-%H-%M-%S"))

    if gobackbtn.clicked():
       menu.currentmenu = "Main Menu"
    import gymcar
    # DRAW GRAPH
    main.screen.blit(draw_graph(main.x_axis,main.y_axis), (720,100))