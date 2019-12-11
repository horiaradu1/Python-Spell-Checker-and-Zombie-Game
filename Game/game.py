from tkinter import *
import random
import time
import math

class gamesprite:
    def __init__(self, x, y, r, image):
        global canvas
        self.rad = r
        self.shape = canvas.create_oval(x-r, y-r, x+r, y+r, outline = "darkgreen")
        self.texture = canvas.create_image(x, y, image = image, anchor=CENTER)
    def move(self, x, y):
        global canvas
        canvas.move(self.shape, x, y)
        canvas.move(self.texture, x, y)
        canvas.focus(self.texture)
    def change_coords(self, x, y):
        global canvas
        canvas.coords(self.shape, x-self.rad, y-self.rad, x+self.rad, y+self.rad)
        canvas.coords(self.texture, x, y)
        canvas.focus(self.texture)
    def delete(self):
        global canvas
        canvas.delete(self.shape)
        canvas.delete(self.texture)
    def distance_from(self, target):
        global canvas
        local_coords = canvas.coords(self.shape)
        local_coords = [(local_coords[0]+local_coords[2])//2,(local_coords[1]+local_coords[3])//2]
        target_coords = canvas.coords(target.shape)
        target_coords = [(target_coords[0]+target_coords[2])//2,(target_coords[1]+target_coords[3])//2]
        return math.sqrt((local_coords[0]-target_coords[0])**2+(local_coords[1]-target_coords[1])**2)
    def collides(self,target):
        global canvas
        distance = self.distance_from(target)
        if distance < self.rad+target.rad:
            return True
        return False
    def image_config(self,image):
        global canvas
        canvas.delete(self.texture)
        local_coords = canvas.coords(self.shape)
        self.texture = canvas.create_image(local_coords[0]+self.rad, local_coords[1]+self.rad, image = image, anchor=CENTER)
    def border(self):
        local_coords = canvas.coords(self.shape)
        if local_coords[1] < 0:  #UP
            self.move(0,height-100)
        elif local_coords[3] > height:   #DOWN
            self.move(0,-height+100)
        elif local_coords[2] > width:    #RIGHT
            self.move(-width+100,0)
        elif local_coords[0] < 0:    #LEFT
            self.move(width-100,0)

class Clock:

    def __init__(self):
        self.start_time = time.time()
        self.pause_time = 0
        self.timer = 21
    def pause(self):
        self.start_pause_time =time.time()
    def unpause(self):
        self.stop_pause_time = time.time()
        self.pause_time += self.stop_pause_time-self.start_pause_time
    def get_time(self):
        self.current_time = time.time()
        return self.timer - (self.current_time-self.start_time-self.pause_time)
    def reinit(self):
        self.start_time = time.time()
        self.pause_time = 0
        self.timer = 21
        self.pause()

def game_window(wsize, hsize):      #This function defines the main window
    game.title("My Game")
    global widthscreen
    global heightscreen
    widthscreen = game.winfo_screenwidth()
    heightscreen = game.winfo_screenheight()
    xvar = (widthscreen/2)-(wsize/2)
    yvar = (heightscreen/2)-(hsize/2)
    game.geometry('%dx%d+%d+%d' % (wsize, hsize, xvar, yvar))
    #game.configure(background='#ffa500')
    return game

def makeFullscreen():
    game.attributes('-fullscreen',False)     #For fullscreen mode, to swith press F11
    game.bind("<F11>", lambda event: game.attributes("-fullscreen", not game.attributes("-fullscreen")))

game = Tk()
global widthscreen
global heightscreen
global width
global height
widthscreen = game.winfo_screenwidth()
heightscreen = game.winfo_screenheight()
width = widthscreen
height = heightscreen

game = game_window(width, height)
canvas = Canvas(game, bg = "darkgreen", relief = "ridge", bd = 20)
canvas.pack(fill = "both", expand = True)

makeFullscreen()

game.mainloop()
