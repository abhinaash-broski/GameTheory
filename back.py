import pygame
import math

sharpness_factor = 1 #may make certain font-sizes abnormal
pygame.init()
pygame.freetype.set_default_resolution(72*sharpness_factor)

processor_relief = 40 #to keep the program healthy

imgloader = {"copycat":"char1","all cooperate":"char2","all cheat":"char3","grudger":"char4","detective":"char5","copykitten":"char6","simpleton":"char7","random":"char8"}

def end(): #to be called when the program is to be terminated
    pygame.quit()
    exit(1)

class Screen: #the main screen
    def __init__(self,initial_size,minimum_size,logo_path,caption,initial_subscreen,navigators={},color_name='red'): #navigators is a dictionary of subscreens
        self.screen = pygame.display.set_mode(initial_size,pygame.RESIZABLE)
        self.size = list(initial_size)
        self.minimum_size = minimum_size
        pygame.display.set_icon(pygame.image.load(logo_path))
        pygame.display.set_caption(caption)
        self.fill_color = color_name 
        self.current_subscreen = initial_subscreen
        self.navigators = navigators
        self.navid = list(navigators.keys()).index(initial_subscreen)
        self.navn = len(self.navigators)
        self.hovering = -1 
        self.active = -1
        self.keypress1 = 0
        self.keypress2 = 0
    def before(self):
        self.screen.fill(self.fill_color)
    def after(self):
        pygame.display.flip()
    def event_handler(self,buttons,reloaders,refresher=0):
        def reloader():
            for f in reloaders:
                f()
        while 1: 
            state_change = 0
            for event in pygame.event.get(): 
                if event.type == pygame.QUIT: #to be called when the program is to be terminated
                    end()
                elif event.type == pygame.VIDEORESIZE: #to be called when the window is resized
                    self.size = list(event.size)
                    if self.size[0]<self.minimum_size[0]:
                        self.size[0] = self.minimum_size[0]
                    if self.size[1]<self.minimum_size[1]:
                        self.size[1] = self.minimum_size[1]
                    self.screen = pygame.display.set_mode(self.size,pygame.RESIZABLE)
                    state_change = 1
                elif event.type == pygame.MOUSEMOTION: #to be called when the mouse is moved
                    mp = pygame.mouse.get_pos()
                    if self.hovering!=-1:
                        if ((buttons[self.hovering][0]) and (not pygame.Rect((buttons[self.hovering][1][0]+self.subscreen_position[0],buttons[self.hovering][1][1]+self.subscreen_position[1],buttons[self.hovering][1][2],buttons[self.hovering][1][3])).collidepoint(mp))):
                            buttons[self.hovering][0]=0
                            self.hovering = -1
                            reloader()
                            state_change = 1
                    else:
                        for i in range(len(buttons)): #to be called when the mouse is moved over a button
                            if pygame.Rect((buttons[i][1][0]+self.subscreen_position[0],buttons[i][1][1]+self.subscreen_position[1],buttons[i][1][2],buttons[i][1][3])).collidepoint(mp):
                                buttons[i][0]=1
                                self.hovering = i
                                reloader()
                                state_change = 1
                                break
                elif event.type == pygame.MOUSEBUTTONDOWN: #to be called when a mouse button is pressed
                    if self.hovering!=-1:
                        if (buttons[self.hovering][0]==1):
                            buttons[self.hovering][0]=2
                            self.active = self.hovering
                            reloader()
                            state_change = 1
                elif event.type == pygame.MOUSEBUTTONUP: #to be called when a mouse button is released
                    if self.active!=-1: 
                        if (buttons[self.active][0]==2 and self.active==self.hovering):
                            buttons[self.active][0]=0
                            reloader()
                            for f in buttons[self.active][8]:
                                f[0](*f[1:])
                            state_change = 1
                elif event.type == pygame.KEYDOWN: #to be called when a key is pressed
                    if event.key == pygame.K_RIGHT: #to be called when the right arrow key is pressed
                        if not self.keypress1 and self.navid<self.navn-1: 
                            self.navid+=1
                            self.current_subscreen = list(self.navigators.keys())[self.navid]
                            self.navigators[self.current_subscreen]()
                            self.switch_section(0,self.current_subscreen)
                        self.keypress1 = 1
                    elif event.key == pygame.K_LEFT:
                        if not self.keypress2 and self.navid>0:  #to be called when the left arrow key is pressed
                            self.navid-=1 
                            self.current_subscreen = list(self.navigators.keys())[self.navid]
                            self.navigators[self.current_subscreen]()
                            self.switch_section(0,self.current_subscreen)
                        self.keypress2 = 1
                elif event.type == pygame.KEYUP:
                    if event.key == pygame.K_RIGHT:
                        self.keypress1 = 0
                    elif event.key == pygame.K_LEFT:
                        self.keypress2 = 0
            if refresher: #to be called when the mouse is moved over a button
                mp = pygame.mouse.get_pos()
                for i in range(len(buttons)):
                    if pygame.Rect((buttons[i][1][0]+self.subscreen_position[0],buttons[i][1][1]+self.subscreen_position[1],buttons[i][1][2],buttons[i][1][3])).collidepoint(mp): 
                        buttons[i][0]=1
                        self.hovering = i
                        reloader()
                        state_change = 1
            if state_change:
                break
            else:
                while not pygame.event.peek():
                    pygame.time.wait(processor_relief) 
                break
    def flush(self): #to be called when the screen is to be cleared
        self.hovering = -1
        self.active = -1
    def place_subscreen(self,subscreen): #to be called when a subscreen is to be placed on the screen
        size_of_subscreen = subscreen.get_size()
        self.subscreen_position = ((self.size[0]-size_of_subscreen[0])/2,(self.size[1]-size_of_subscreen[1])/2)
        self.screen.blit(subscreen,self.subscreen_position)
    def switch_section(self,f,t,do_not_handle=0): #to be called when a subscreen is to be switched
        self.current_subscreen = t
        if f!=0:
            f.enabled = False
        else:
            for Li in list(self.navigators.keys()):
                Li.enabled = False
        t.enabled = True
        self.flush()
        t.ready_static()
        t.ready_objects()
        t.ready_dynamic()
        self.before()
        self.place_subscreen(t.return_subscreen())
        self.after()
        if not do_not_handle:
            self.event_handler(t.buttons,[t.ready_objects,t.ready_dynamic],1)

class Section: #a subscreen
    def __init__(self,size,color_name,caption="",initial_state=False): 
        self.background = pygame.Surface(size)
        self.background.fill(color_name)
        self.background_color = color_name
        self.caption = caption
        self.enabled = initial_state
        self.labels = []
        self.buttons = []
        self.objects = []
        self.active_position = [0,0]
    #For new label, offset = 0; For new line offset = line gap in terms of font size; For continuation offset = -1; For horizontally centering single label, offset = -2
    def add_label(self,text,text_color,font_name,font_size,position,offset=-1,italic=False,bold=False,background_color="yellow"):
        font_object = pygame.freetype.SysFont(font_name,int(font_size/sharpness_factor),bold=bold,italic=italic) 
        font_object.antialiased = True
        img = font_object.render(text,text_color,bgcolor=background_color)[0]
        if (offset==0): 
            self.active_position= [position[0],position[1]]
        elif (offset==-2):
            self.active_position = [position[0]-(img.get_width()/2),position[1]]
        elif (offset!=-1):
            self.active_position= [position[0],self.active_position[1]+offset*font_size]
        copy_position = (self.active_position[0],self.active_position[1])
        self.labels.append([img,copy_position,text])
        self.active_position[0]+=img.get_width()
    def remove_label(self,text): 
        for label in self.labels:
            if label[2]==text:
                self.labels.remove(label)
    def add_button(self,text,text_color,font_name,font_size,rect,passive_bg,hover_bg,active_bg,border_color,funcset,border_width=1):
        font_object = pygame.freetype.SysFont(font_name,int(font_size/sharpness_factor))
        font_object.antialiased = True
        self.buttons.append([0,rect,[text,text_color,font_object],passive_bg,hover_bg,active_bg,border_color,border_width,funcset])
        #First integer: 0=none, 1=hover, 2=active
    def remove_button(self,text):
        for button in self.buttons:
            if button[2][0]==text:
                self.buttons.remove(button)
                break
    def config_machine(self,rect,left,right,top,bottom,leftn=None,rightn=None,topn=None,bottomn=None,color="blue"): #left,right,top,bottom are booleans
        for obj in self.objects:
            if obj[2]=="machine":
                self.objects.remove(obj)
        mach = pygame.Surface((rect[2],rect[3]))
        mach.fill(color)
        backcolors = ["white","yellow"] #white=cooperate, yellow=cheat
        pygame.draw.polygon(mach,backcolors[top],[(125,20),(165,60),(125,100),(85,60)]) #square
        pygame.draw.polygon(mach,backcolors[right],[(165,60),(205,100),(165,140),(125,100)]) #square
        pygame.draw.polygon(mach,backcolors[bottom],[(125,100),(165,140),(125,180),(85,140)]) #square
        pygame.draw.polygon(mach,backcolors[left],[(85,60),(125,100),(85,140),(45,100)]) #square
        pygame.draw.polygon(mach,"black",[(125,20),(205,100),(125,180),(45,100)],width=5) #square
        pygame.draw.lines(mach,"black",True,[(165,140),(85,60),(85,140),(165,60)],width=5) #cross
        pygame.draw.line(mach,"black",(125,20),(125,180),width=5) #vertical
        capt_obj = pygame.freetype.SysFont("consolas",12) #captions
        mach.blits(((capt_obj.render("you",fgcolor="black",rotation=45)[0],(35,60)),(capt_obj.render("cheat",fgcolor="black",rotation=45)[0],(40,65)),(capt_obj.render("you",fgcolor="black",rotation=45)[0],(75,20)),(capt_obj.render("cooperate",fgcolor="black",rotation=45)[0],(70,15)),(capt_obj.render("they",fgcolor="black",rotation=-45)[0],(150,10)),(capt_obj.render("cooperate",fgcolor="black",rotation=-45)[0],(130,10)),(capt_obj.render("they",fgcolor="black",rotation=-45)[0],(190,50)),(capt_obj.render("cheat",fgcolor="black",rotation=-45)[0],(180,60)))) 
        num_obj = pygame.freetype.SysFont("bahnschrift",24) 
        if (bottomn==None and bottom) or (bottomn): 
            mach.blits(((num_obj.render("0")[0],(105,130)),(num_obj.render("0")[0],(135,130))))
        if (topn==None and top) or (topn):
            mach.blits(((num_obj.render("+2")[0],(97,50)),(num_obj.render("+2")[0],(129,50))))
        if (leftn==None and left) or (leftn):
            mach.blits(((num_obj.render("+3")[0],(57,90)),(num_obj.render("-1")[0],(90,90))))
        if (rightn==None and right) or (rightn):
            mach.blits(((num_obj.render("-1")[0],(138,90)),(num_obj.render("+3")[0],(169,90))))
        self.objects.append([mach,rect,"machine"])
    def add_player(self,character,position,dir=0): #dir=0 for left, dir=1 for right
        img = pygame.image.load(character+".png")
        if dir: 
            img = pygame.transform.flip(img,1,0)
        self.objects.append([img,position,character])
    def config_circle(self,charlist,scorelist,radius,rect,highlight=-1,linecolor="black"): #charlist and scorelist are lists of characters and scores respectively
        w,h = rect[2],rect[3]
        circlesurf = pygame.Surface((w,h))
        circlesurf.fill("white")
        n = len(charlist)
        theta = 2*math.pi/n
        points = []
        for i in range(n): #to be called when a circle is to be drawn
            points.append(((w/2)+radius*math.cos(i*theta),(h/2)+radius*math.sin(i*theta))) 
        for i in range(n): 
            for j in range(i+1,n): 
                pygame.draw.aaline(circlesurf,linecolor,points[i],points[j]) 
        if highlight!=-1: 
            for i in range(n):
                pygame.draw.aaline(circlesurf,"yellow",points[i],points[highlight],blend=2) #to be called when a line is to be highlighted
        font_object = pygame.freetype.SysFont("bahnschrift",16)
        for i in range(n): 
            img = font_object.render("%d"%scorelist[i])[0]
            circlesurf.blit(img,((w/2)+(radius+20)*math.cos(i*theta)-(img.get_width()/2),(h/2)+(radius+20)*math.sin(i*theta)-(img.get_height()/2)))
        for i in  range(n):
            img = pygame.transform.scale(pygame.image.load(imgloader[charlist[i]]+".png"),(30,35)) #to be called when a character is to be drawn
            circlesurf.blit(img,((w/2)+(radius+55)*math.cos(i*theta)-(img.get_width()/2),(h/2)+(radius+55)*math.sin(i*theta)-(img.get_height()/2)))
        self.objects.append([circlesurf,rect,"circle"])
    def config_sandbox(self,rect,sandcolor="green",tab=0): #tab=0 for left, tab=1 for right
        sand = pygame.Surface((rect[2],rect[3])) 
        sand.fill(sandcolor)
        self.objects.append([sand,rect,"sandbox"])
    def ready_static(self): #to be called when the screen is to be prepared
        self.background.fill(self.background_color)
        for label in self.labels:
            self.background.blit(label[0],label[1])
    def ready_dynamic(self): #to be called when the screen is to be prepared
        for button in self.buttons: #to be called when a button is to be drawn
            if button[0]==0:
                pygame.draw.rect(self.background,button[3],button[1],border_radius=int(button[1][1]/2))
                text_img = button[2][2].render(button[2][0],button[2][1],bgcolor=button[3])[0]
            elif button[0]==1:
                pygame.draw.rect(self.background,button[4],button[1],border_radius=int(button[1][1]/2))
                text_img = button[2][2].render(button[2][0],button[2][1],bgcolor=button[4])[0]
            elif button[0]==2:
                pygame.draw.rect(self.background,button[5],button[1],border_radius=int(button[1][1]/2))
                text_img = button[2][2].render(button[2][0],button[2][1],bgcolor=button[5])[0] 
            pygame.draw.rect(self.background,button[6],button[1],width=button[7],border_radius=int(button[1][1]/2))
            self.background.blit(text_img,(button[1][0]+((button[1][2]-text_img.get_width())/2),button[1][1]+((button[1][3]-text_img.get_height())/2)))
    def ready_objects(self): #to be called when the screen is to be prepared
        for obj in self.objects:
            self.background.blit(obj[0],obj[1])
    def flush(self): #to be called when the screen is to be cleared
        self.objects=[]
        self.labels=[]
        self.buttons=[]
    def reset(self): #to be called when the screen is to be reset
        pass
    def return_subscreen(self): #to be called when the screen is to be returned
        return self.background

class TempValues: #to be called when temporary values are to be stored
    def __init__(self):
        pass