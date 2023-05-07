import menu
from datetime import datetime
import time
import matplotlib as mpl
import matplotlib.pyplot as plt
import matplotlib.backends.backend_agg as agg
import numpy as np
import pygame




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
    plt.close()
    surf = pygame.image.fromstring(raw_data, (width,height), "RGB")
    return surf

renderbool = True
renderbool2 = True
# Some ui elements (get drawn later)
gobackbtn = menu.Button(780+25,620,100,50,"Go Back")
savemodelbtn = menu.Button(780+100*1+10+25,620,100,50,"Save Model")
renderbtn = menu.Button(780+100*2+10*2+25,620,100,50,"Render:    ")
raysbtn = menu.Button(805+100*3+10*3+25,620,150,50,"Rays & Checks:    ")
# On and off text
on = menu.Text("On",16,(0,255,0))
off = menu.Text("Off", 16,(255,0,0))
on1 = menu.Text("On",16,(0,255,0))
off1 = menu.Text("Off", 16,(255,0,0))
def ui_elements(render_graph=True,save_model=True):
    global renderbool, renderbool2
    
    # If rendering is turned off
    if renderbtn.clicked():
        renderbool ^= True
        time.sleep(0.5)

    # If rendering of checkpoints and rays are off
    if raysbtn.clicked():
        renderbool2 ^= True
        time.sleep(0.5)
    

    # Render some nice text
    menu.Text("AI Car Simulator",64).draw(720+280,50)
    
    # Render buttons 
    if save_model:
        savemodelbtn.draw()
    gobackbtn.draw()
    renderbtn.draw()
    raysbtn.draw()
    

    if renderbool:
        on.draw((780+100*2+10*2+30+25,620))
    else:
        off.draw((780+100*2+10*2+30+25,620))

    if renderbool2:
        on1.draw((805+100*3+10*3+55+25,620))
    else:
        off1.draw((805+100*3+10*3+55+25,620))
        
    from main import model, x_axis,y_axis,screen
    if save_model:
        if savemodelbtn.clicked():
            # Save the current model with the date and time
            model.save("models/air-car-model-"+datetime.now().strftime("%d-%m-%Y-%H-%M-%S"))

    if gobackbtn.clicked():
       menu.currentmenu = "Main Menu"
       menu.file_prompted = False
    # DRAW GRAPH
    if render_graph:
        screen.blit(draw_graph(x_axis,y_axis), (720,100))

def game_load(new_model,vec_env,obs):
    # Run pretained model
    action, _states = new_model.predict(obs)
    obs, rewards, dones, info = vec_env.step(action)
    for idx, env in enumerate(vec_env.envs):
        if idx == 0:
            env.render()
        else:
            env.onlycar()
    ui_elements(save_model=False,render_graph=False)

def game():
    # Train the model
    from main import model, env
    model.learn(total_timesteps=1, reset_num_timesteps=False)
    if renderbool:
        for idx, env in enumerate(env.envs):
            if idx == 0:
                env.render()
            else:
                env.onlycar()
    ui_elements()

