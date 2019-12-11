from tkinter import *
import random
import time
import math

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
