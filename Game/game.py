from tkinter import *
import random
import time
import math
import pickle

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

class Bullet(gamesprite):
    def __init__(self,x,y,r,image):
        global canvas
        global game
        gamesprite.__init__(self,x,y,r,image)
        self.shot_time = 0
        self.stop = False
        if Player.direction == "left":
            self.shootX = -10
            self.shootY = 0
        elif Player.direction == "right":
            self.shootX = 10
            self.shootY = 0
        elif Player.direction == "up":
            self.shootX = 0
            self.shootY = -10
        elif Player.direction == "down":
            self.shootX = 0
            self.shootY = +10
        game.after(20, self.shooting_move)

    def shooting_move(self):
        global canvas
        global game
        global score
        global scoretxt
        global end
        global gamePaused
        global maxshots
        global ammotxt

        if gamePaused == False:
            self.move(self.shootX, self.shootY)
            self.shot_time += 1
            if self.shot_time == 180:
                self.stop = True
            if end == True:
                self.stop = True
            if self.stop == False:
                try:
                    for oneenemy in Enemy:
                        if self.collides(oneenemy):
                            score = score + 1
                            game_timer.timer = game_timer.timer + 1
                            coords = random_enemy()
                            oneenemy.change_coords(coords[0], coords[1])
                            canvas.delete(scoretxt)
                            scoretxt = canvas.create_text(150,50,anchor=N,font=("Purisa",30),text="Score: " + str(int((score))))
                            self.stop = True
                            break
                except IndexError:
                    pass
                canvas.update()
                game.after(10, self.shooting_move)
            else:
                self.delete()
        else:
            canvas.update()
            game.after(10, self.shooting_move)

class makeEnemy(gamesprite):

    def __init__(self, x, y, r, image):
        global canvas
        gamesprite.__init__(self,x,y,r,image)
        self.moving = True
        self.zdirection = random.randint(0,3)
        self.counter = random.randint(4,10)
        self.moveEnemy()

    def start(self):
        self.moving = True
    def stop(self):
        self.moving = False

    def moveEnemy(self):
        global end
        global score
        global width
        global height
        global endtxt
        if self.collides(Player):
            end = True
            endtxt = canvas.create_text(width//2,height//1.5,anchor=N, font=("Purisa",30),text="Game Over! You killed " + str(score) + " zombies and died")
            Player.change_coords(width//2, height//2)
            for oneenemy in Enemy:
                coords = random_enemy()
                oneenemy.change_coords(coords[0], coords[1])

        random_time = random.randint(100,200)
        if self.moving:
            if self.counter == 0:
                self.zdirection = random.randint(0,3)
                self.counter = random.randint(4,10)
            self.zdistance = random.randint(10,20)
            game.after(random_time, self.moveEnemy)
            if self.zdirection == 0:
                self.move(-self.zdistance,0)
                self.image_config(image=enemyleft)
            elif self.zdirection == 1:
                self.move(+self.zdistance,0)
                self.image_config(image=enemyright)
            elif self.zdirection == 2:
                self.move(0,-self.zdistance)
                self.image_config(image=enemyup)
            elif self.zdirection == 3:
                self.move(0,+self.zdistance)
                self.image_config(image=enemydown)
            self.border()
            self.counter -= 1
        else:
            game.after(20,self.moveEnemy)


class makePlayer(gamesprite):

    def shoot(self, event):
        global maxshots
        global ammotxt
        global reload_done
        if gamePaused == False and end == False and maxshots < 10 and reload_done == True:
            local_coords = canvas.coords(self.shape)
            if self.direction == "left":
                Bullets.append(Bullet(local_coords[0]+self.rad, local_coords[1]+self.rad, 10, bulletleft))
            elif self.direction == "right":
                Bullets.append(Bullet(local_coords[0]+self.rad, local_coords[1]+self.rad, 10, bulletright))
            elif self.direction == "up":
                Bullets.append(Bullet(local_coords[0]+self.rad, local_coords[1]+self.rad, 10, bulletup))
            elif self.direction == "down":
                Bullets.append(Bullet(local_coords[0]+self.rad, local_coords[1]+self.rad, 10, bulletdown))
            maxshots += 1
            try:
                canvas.delete(ammotxt)
            except NameError:
                pass
            ammotxt = canvas.create_text(175,100,anchor=N,font=("Purisa",30),text="Ammo: {0}/10".format(10-maxshots))

    def reload_timer(self, event):
        global reload_done
        global reloadtxt
        if reload_done == True and gamePaused == False and end == False:
            reload_done = False
            reloadtxt = canvas.create_text(width/2,height/2,anchor=N,font=("Purisa",25),text="Reloading...")
            game.after(2000, self.reload)

    def reload(self):
        global maxshots
        global ammotxt
        global reload_done
        global reloadtxt
        if gamePaused == False:
            maxshots = 0
            canvas.delete(ammotxt)
            ammotxt = canvas.create_text(175,100,anchor=N,font=("Purisa",30),text="Ammo: {0}/10".format(10-maxshots))
            reload_done = True
            canvas.delete(reloadtxt)
        else:
            game.after(2000, self.reload)

    def __init__(self, x, y, r, image):
        global canvas
        gamesprite.__init__(self,x,y,r,image)
        self.direction = "down"
        self.velocity = 0
        canvas.bind("<space>", self.shoot)
        canvas.bind("<r>", self.reload_timer)
        canvas.bind("<R>", self.reload_timer)
        canvas.bind("<KeyPress>", self.keypressed)
        canvas.bind("<KeyRelease>", self.keyreleased)
        canvas.focus_set()

    def movePlayer(self):
        if self.direction == "left":
            self.move(-self.velocity,0)
            self.image_config(image=playerleft)
        elif self.direction == "right":
            self.move(+self.velocity,0)
            self.image_config(image=playerright)
        elif self.direction == "up":
            self.move(0,-self.velocity)
            self.image_config(image=playerup)
        elif self.direction == "down":
            self.move(0,+self.velocity)
            self.image_config(image=playerdown)
        self.border()

    def keypressed(self, event):
        if event.char == "a" or event.char == "A":
            self.direction = "left"
        elif event.char == "d" or event.char == "D":
            self.direction = "right"
        elif event.char == "w" or event.char == "W":
            self.direction = "up"
        elif event.char == "s" or event.char == "S":
            self.direction = "down"
        if event.char in ["w", "a", "s", "d", "W", "A", "S", "D"]:
            self.velocity = 8

    def keyreleased(self, event):
        self.velocity = 0

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

def pause(event):
    global gamePaused
    global pausetxt
    global canvas
    global end
    global menu
    global countdown

    if not end:
        if gamePaused and countdown == False:
            try:
                canvas.delete(pausetxt)
            except NameError:
                pass
            try:
                menu.destroy()
            except NameError:
                pass
            ready_timer(3, None)
            countdown = True
        elif not gamePaused and countdown == False:
            game_timer.pause()
            pausetxt = canvas.create_text(width//2,height//1.5,anchor=N, font=("Purisa",40),text="Game Paused")
            gamePaused = not gamePaused


def ready_timer(time, text):
    global gamePaused
    global canvas
    global scoretxt
    global ammotxt
    global countdown
    if time > 0:
        if text != None:
            canvas.delete(text)
        text = canvas.create_text(width//2,height//1.5,anchor=N, font=("Purisa",40),text="Game resuimg in " + str(time) + " seconds...")
        game.after(1000, lambda tr=time-1, txt=text: ready_timer(tr, txt))
    else:
        canvas.delete(text)
        gamePaused = not gamePaused
        game_timer.unpause()
        for oneenemy in Enemy:
            oneenemy.start()
        canvas.delete(scoretxt)
        canvas.delete(ammotxt)
        scoretxt = canvas.create_text(150,50,anchor=N,font=("Purisa",30),text="Score: " + str(int((score))))
        ammotxt = canvas.create_text(175,100,anchor=N,font=("Purisa",30),text="Ammo: {0}/10".format(10-maxshots))
        countdown = False

def game_loop():
    global end
    global width
    global height
    global timertxt
    global scoretxt
    global maxshots
    global endtxt

    if end == False and gamePaused == False:
        Player.movePlayer()
        try:
            canvas.delete(timertxt)
        except NameError:
            pass
        timertxt = canvas.create_text(width-200,height/16,anchor=N,font=("Purisa",30),text="Time left: " + str(int((game_timer.get_time()))))

        if int(game_timer.get_time()) == 0:
            end = True
            endtxt = canvas.create_text(width//2,height//1.5,anchor=N, font=("Purisa",30),text="Time is up! You killed " + str(score) + " zombies")
            Player.change_coords(width//2, height//2)
            for oneenemy in Enemy:
                coords = random_enemy()
                oneenemy.change_coords(coords[0], coords[1])
            dump_leaderboard()
            restart_vars()
            mainmenu()

        random_time = random.randint(200,500)
        game.update()
        time.sleep(.001)

        height = canvas.winfo_height()
        width = canvas.winfo_width()

    else:
        for oneenemy in Enemy:
           oneenemy.stop()

    game.after(20,game_loop)

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

bossimg = PhotoImage(file = "images/bossimage.png")

imgup = PhotoImage(file = "images/playerup.png")
playerup = imgup.subsample(3, 3)
imgdown = PhotoImage(file = "images/playerdown.png")
playerdown = imgdown.subsample(3, 3)
imgleft = PhotoImage(file = "images/playerleft.png")
playerleft = imgleft.subsample(3, 3)
imgright = PhotoImage(file = "images/playerright.png")
playerright = imgright.subsample(3, 3)

eimgup = PhotoImage(file = "images/enemyup.png")
enemyup = eimgup.subsample(4, 4)
eimgdown = PhotoImage(file = "images/enemydown.png")
enemydown = eimgdown.subsample(4, 4)
eimgleft = PhotoImage(file = "images/enemyleft.png")
enemyleft = eimgleft.subsample(4, 4)
eimgright = PhotoImage(file = "images/enemyright.png")
enemyright = eimgright.subsample(4, 4)

bimgup = PhotoImage(file = "images/bulletup.png")
bulletup = bimgup.subsample(4, 4)
bimgdown = PhotoImage(file = "images/bulletdown.png")
bulletdown = bimgdown.subsample(4, 4)
bimgleft = PhotoImage(file = "images/bulletleft.png")
bulletleft = bimgleft.subsample(4, 4)
bimgright = PhotoImage(file = "images/bulletright.png")
bulletright = bimgright.subsample(4, 4)

global gamePaused
global end
global score
global zombie_nr
global maxshots
global reload_done
global Player
global Enemy
global countdown
global game_timer

score = 0
zombie_nr = 6
maxshots = 0
gamePaused = False
end = False
reload_done = True
username = None
countdown = False
game_timer = Clock()
game_timer.pause()

Enemy = list()
Bullets = list()

Player = makePlayer(width/2, height/2, 50, playerdown)

game_loop()
game.mainloop()
