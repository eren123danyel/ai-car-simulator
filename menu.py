from multipledispatch import dispatch
import tkinter
import tkinter.filedialog
import pygame

def import_screen():
    from main import screen
    return screen

def prompt_file():
    top = tkinter.Tk()
    top.iconbitmap(default="green-car.ico")
    top.withdraw()  # hide window
    file_name = tkinter.filedialog.askopenfilename(parent=top,title="Choose model",filetypes=[("Zip files",'.zip')])
    top.destroy()
    return file_name

class Text:
    def __init__(self,text,fontsize,color=(255,255,255)):
        # defining a font
        smallfont = pygame.font.SysFont('Corbel',fontsize)
        # render text
        self.text = smallfont.render(text , True , color)
    @dispatch((float,int),(float,int))
    def draw(self,posx,posy):
        # Draw from the center
        posx = posx - (self.text.get_rect().width/2)
        posy = posy - (self.text.get_rect().height/2)
        screen.blit(self.text,(posx,posy))
    
    @dispatch(tuple)
    def draw(self,pos):
        # Draw from the center
        posx = pos[0] - (self.text.get_rect().width/2)
        posy = pos[1] - (self.text.get_rect().height/2)
        screen.blit(self.text,(posx,posy))


class Button:
    def __init__(self,posx,posy,sizex,sizey,text,textsize=16):
        # Draw the button from the center instead of the corner
        self.posx = posx - (sizex/2)
        self.posy = posy - (sizey/2)
        self.sizex = sizex
        self.sizey = sizey
        # Set the name of the menu
        self.menu = text
        # Render text
        self.text = Text(text,textsize).text
        self.darkColor = (100,100,100)
        self.lightColor = (170,170,170)
        self.rect = pygame.Rect(self.posx,self.posy,self.sizex,self.sizey)
    
    def draw(self):
        mouse = pygame.mouse.get_pos()
        #width,height = (main.screen.get_width(),main.screen.get_height())
        # Change color if mouse is hovering
        if self.rect.collidepoint(mouse):
            pygame.draw.rect(screen,self.lightColor,[self.posx,self.posy,self.sizex,self.sizey])
        else:
            pygame.draw.rect(screen,self.darkColor,[self.posx,self.posy,self.sizex,self.sizey])
        # Write text in the center
        screen.blit(self.text, ((self.posx+(self.sizex/2))-(self.text.get_rect().width/2),(self.posy+(self.sizey/2))-(self.text.get_rect().height/2)))
    
    def clicked(self):
        mouse = pygame.mouse.get_pos()
        # Check if mouse is inside the bounding of the button 
        if pygame.mouse.get_pressed()[0] and self.rect.collidepoint(mouse):
            return True
        return False

file_prompted = False
def start(i):
    from game import game, game_load
    global file_prompted, new_model, vec_env, obs
    if i == 1:
        game()
    elif i == 2:
        if not file_prompted:
            #get the name of the file
            file_name = prompt_file()
            from main import model, DQN
            new_model = DQN.load(file_name)
            vec_env = model.get_env()
            obs = vec_env.reset()
            file_prompted = True
        #Load presaved model
        game_load(new_model,vec_env,obs)

def quit():
    pygame.quit()


currentmenu = "Main Menu"
def mainmenu():
    global screen
    screen = import_screen()
    # Make sure currentmenu is available out-of-scope
    global currentmenu
    buttons = []
    # Width and height
    width, height = (1280,720)
    # Title
    Text("AI Car Simulator",64,(0,0,0)).draw(width/2,100)
    # Define sizes
    btnx = 200
    btny = 100
    # First button
    buttons.append(Button(width/2,height/3,btnx,btny,"Start",32))
    # Second button
    buttons.append(Button(width/2,height/3+btny*1.1+10,btnx,btny,"Load Saved",32))
    # Third button
    buttons.append(Button(width/2,height/3+btny*2.2+10*2,btnx,btny,"Quit",32))
    for btn in buttons:
        # Render button
        btn.draw()
        # if the button is draw, change to that menu
        if btn.clicked():
            currentmenu = btn.menu
def menu():
    # Render which ever menu is running
    if currentmenu == "Main Menu":
        mainmenu()
    elif currentmenu == "Start":
        start(1)
    elif currentmenu == "Quit":
        quit()
    elif currentmenu == "Load Saved":
        start(2)

    
