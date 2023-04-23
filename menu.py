from multipledispatch import dispatch

class Text:
    def __init__(self,text,fontsize,color=(255,255,255)):
        import main
        # define a screen
        self.screen = main.screen
        # defining a font
        pygame = main.pygame
        smallfont = pygame.font.SysFont('Corbel',fontsize)
        # render text
        self.text = smallfont.render(text , True , color)
    @dispatch((float,int),(float,int))
    def draw(self,posx,posy):
        # Draw from the center
        posx = posx - (self.text.get_rect().width/2)
        posy = posy - (self.text.get_rect().height/2)
        self.screen.blit(self.text,(posx,posy))
    
    @dispatch(tuple)
    def draw(self,pos):
        # Draw from the center
        posx = pos[0] - (self.text.get_rect().width/2)
        posy = pos[1] - (self.text.get_rect().height/2)
        self.screen.blit(self.text,(posx,posy))


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
    
    def draw(self):
        import main
        pygame = main.pygame
        mouse = pygame.mouse.get_pos()
        #width,height = (main.screen.get_width(),main.screen.get_height())
        # Change color if mouse is hovering
        if self.posx <= mouse[0] <= self.posx+self.sizex and self.posy <= mouse[1] <= self.posy+self.sizey:
            pygame.draw.rect(main.screen,self.lightColor,[self.posx,self.posy,self.sizex,self.sizey])
        else:
            pygame.draw.rect(main.screen,self.darkColor,[self.posx,self.posy,self.sizex,self.sizey])
        # Write text in the center
        main.screen.blit(self.text, ((self.posx+(self.sizex/2))-(self.text.get_rect().width/2),(self.posy+(self.sizey/2))-(self.text.get_rect().height/2)))
    
    def clicked(self):
        import main
        pygame = main.pygame
        mouse = pygame.mouse.get_pos()
        mouse_clicked = pygame.mouse.get_pressed(num_buttons=3)
        # Check if mouse is inside the bounding of the button
        if self.posx <= mouse[0] <= self.posx+self.sizex and self.posy <= mouse[1] <= self.posy+self.sizey:
            # Check if the mouse is pressed while inside the button else return False
            if mouse_clicked == (1,0,0):
                return True
            else:
                return False
        else:
            return False

def start():
    import game
    game.game()

def quit():
    import main
    main.pygame.quit()


currentmenu = "Main Menu"
def mainmenu():
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
        start()
    elif currentmenu == "Quit":
        quit()

    
