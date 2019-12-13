from tkinter import *
import random
import time
import math
import pickle


class gamesprite:  # Class for every object in the game
    def __init__(  # Function to initialize it, both its shape and texture
            self,
            x,
            y,
            r,
            image,
    ):
        global canvas
        self.rad = r
        self.shape = canvas.create_oval(
            x - r, y - r, x + r, y + r, outline='darkgreen')
        self.texture = canvas.create_image(x, y, image=image, anchor=CENTER)

    def move(self, x, y):  # Function to move the game object/sprite
        global canvas
        canvas.move(self.shape, x, y)
        canvas.move(self.texture, x, y)
        canvas.focus(self.texture)

    def change_coords(self, x, y):  # Function to relocate the object
        global canvas
        canvas.coords(self.shape, x - self.rad, y - self.rad, x + self.rad,
                      y + self.rad)
        canvas.coords(self.texture, x, y)
        canvas.focus(self.texture)

    def delete(self):  # Function to delete the object
        global canvas
        canvas.delete(self.shape)
        canvas.delete(self.texture)

    def distance_from(
            self, target
    ):  # Function to get the distance from the object to anything
        global canvas
        local_coords = canvas.coords(self.shape)
        local_coords = [(local_coords[0] + local_coords[2]) // 2,
                        (local_coords[1] + local_coords[3]) // 2]
        target_coords = canvas.coords(target.shape)
        target_coords = [(target_coords[0] + target_coords[2]) // 2,
                         (target_coords[1] + target_coords[3]) // 2]
        return math.sqrt((local_coords[0] - target_coords[0])**2 +
                         (local_coords[1] - target_coords[1])**2)

    def collides(self, target):  # Function to check for collision
        global canvas
        distance = self.distance_from(target)
        if distance < self.rad + target.rad:
            return True
        return False

    def image_config(self, image):  # Function to change the image of a object
        global canvas
        canvas.delete(self.texture)
        local_coords = canvas.coords(self.shape)
        self.texture = canvas.create_image(
            local_coords[0] + self.rad,
            local_coords[1] + self.rad,
            image=image,
            anchor=CENTER)

    def border(
            self
    ):
        # Function to check if the object hits the border
        local_coords = canvas.coords(self.shape)
        if local_coords[1] < 0:  # UP
            self.move(0, height - 100)
        elif local_coords[3] > height:

            # DOWN

            self.move(0, -height + 100)
        elif local_coords[2] > width:

            # RIGHT

            self.move(-width + 100, 0)
        elif local_coords[0] < 0:

            # LEFT

            self.move(width - 100, 0)


class Clock:  # Class for the clock/timer
    def __init__(self):  # Begins the block
        self.start_time = time.time()
        self.pause_time = 0
        self.timer = 21

    def pause(self):  # Starts counting the the pause was initialized
        self.start_pause_time = time.time()

    def unpause(self):  # Gets the time when the clock is unpaused the clock
        self.stop_pause_time = time.time()
        self.pause_time += self.stop_pause_time - self.start_pause_time

    def get_time(self):  # Calculates the overall time
        self.current_time = time.time()
        return self.timer - (
            self.current_time - self.start_time - self.pause_time)

    def reinit(self):  # Reinitializez the clock
        self.start_time = time.time()
        self.pause_time = 0
        self.timer = 21
        self.pause()


class Bullet(gamesprite):  # Class for the bullet
    # Initializes the bullet based on the direction of the player
    def __init__(
            self,
            x,
            y,
            r,
            image,
    ):
        global canvas
        global game
        gamesprite.__init__(self, x, y, r, image)
        self.shot_time = 0
        self.stop = False
        if Player.direction == 'left':
            self.shootX = -10
            self.shootY = 0
        elif Player.direction == 'right':
            self.shootX = 10
            self.shootY = 0
        elif Player.direction == 'up':
            self.shootX = 0
            self.shootY = -10
        elif Player.direction == 'down':
            self.shootX = 0
            self.shootY = +10
        game.after(20, self.shooting_move)

    def shooting_move(self):  # Moves each bullet
        global canvas
        global game
        global score
        global scoretxt
        global end
        global gamePaused
        global maxshots
        global ammotxt
        global extra_zombies

        if gamePaused is False:
            self.move(self.shootX, self.shootY)
            self.shot_time += 1
            if self.shot_time == 200:
                self.stop = True
            if end is True:
                self.stop = True
            if self.stop is False:
                try:
                    for oneenemy in Enemy:
                        if self.collides(
                                oneenemy
                        ):  # Checks for each bullet if it hit a enemy
                            score = score + 1
                            game_timer.timer = game_timer.timer + 1
                            coords = random_enemy()
                            oneenemy.change_coords(coords[0], coords[1])
                            canvas.delete(scoretxt)
                            scoretxt = canvas.create_text(
                                150,
                                50,
                                anchor=N,
                                font=('Purisa', 30),
                                text='Score: ' + str(int(score)))
                            self.stop = True
                            difficulty = random.randint(0, 10)
                            if difficulty <= 3:
                                coords = random_enemy()
                                Enemy.append(
                                    makeEnemy(coords[0], coords[1], 50,
                                              enemyup))
                                extra_zombies += 1
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


class makeEnemy(gamesprite):  # Class for each enemy
    def __init__(  # Initializes the enemy
            self,
            x,
            y,
            r,
            image,
    ):
        global canvas
        gamesprite.__init__(self, x, y, r, image)
        self.moving = True
        self.zdirection = random.randint(0, 3)
        self.counter = random.randint(4, 10)
        self.moveEnemy()

    def start(self):  # Starts it moving
        self.moving = True

    def stop(self):  # Stops it from moving
        self.moving = False

    def moveEnemy(self):  # Moves each enemy randomly
        global end
        global score
        global width
        global height
        global endtxt
        global Enemy
        try:
            if self.collides(Player):  # Checks if the enemy hits the player
                end = True
                endtxt = canvas.create_text(
                    width // 2,
                    height // 1.5,
                    anchor=N,
                    font=('Purisa', 30),
                    text='Game Over! You killed ' + str(score) +
                    ' zombies and died')
                Player.change_coords(width // 2, height // 2)
                for oneenemy in Enemy:
                    oneenemy.delete()
                dump_leaderboard()
                restart_vars()
                mainmenu()
            random_time = random.randint(100, 150)
            if self.moving:  # Then moves it randomly
                if self.counter == 0:
                    self.zdirection = random.randint(0, 3)
                    self.counter = random.randint(3, 7)
                self.zdistance = random.randint(10, 20)

                if self.zdirection == 0:
                    self.move(-self.zdistance, 0)
                    self.image_config(image=enemyleft)
                elif self.zdirection == 1:
                    self.move(+self.zdistance, 0)
                    self.image_config(image=enemyright)
                elif self.zdirection == 2:
                    self.move(0, -self.zdistance)
                    self.image_config(image=enemyup)
                elif self.zdirection == 3:
                    self.move(0, +self.zdistance)
                    self.image_config(image=enemydown)
                self.border()
                self.counter -= 1
                game.after(random_time, self.moveEnemy)
            else:
                game.after(20, self.moveEnemy)
        except IndexError:
            pass


class makePlayer(gamesprite):
    def shoot(self, event):  # Event function for shooting
        global maxshots
        global ammotxt
        global reload_done
        if (gamePaused is False and end is False and
                maxshots < 10 and reload_done is True):
            local_coords = canvas.coords(self.shape)
            if self.direction == 'left':
                Bullets.append(
                    Bullet(local_coords[0] - 15,
                           local_coords[1] + self.rad - 15, 10, bulletleft))
            elif self.direction == 'right':
                Bullets.append(
                    Bullet(local_coords[0] + 2 * self.rad + 15,
                           local_coords[1] + self.rad + 15, 10, bulletright))
            elif self.direction == 'up':
                Bullets.append(
                    Bullet(local_coords[0] + self.rad + 15,
                           local_coords[1] - 15, 10, bulletup))
            elif self.direction == 'down':
                Bullets.append(
                    Bullet(local_coords[0] + self.rad - 15,
                           local_coords[1] + 2 * self.rad + 15, 10,
                           bulletdown))
            maxshots += 1
            try:
                canvas.delete(ammotxt)
            except NameError:
                pass
            ammotxt = canvas.create_text(
                175,
                100,
                anchor=N,
                font=('Purisa', 30),
                text='Ammo: {0}/10'.format(10 - maxshots))

    def reload_timer(self, event):  # Event function for reloading
        global reload_done
        global reloadtxt
        if reload_done is True and gamePaused is False and end is False:
            reload_done = False
            reloadtxt = canvas.create_text(
                width / 2,
                height / 2,
                anchor=N,
                font=('Purisa', 25),
                text='Reloading...')
            game.after(2000, self.reload)

    def reload(self):  # Reloading function
        global maxshots
        global ammotxt
        global reload_done
        global reloadtxt
        if gamePaused is False:
            maxshots = 0
            canvas.delete(ammotxt)
            ammotxt = canvas.create_text(
                175,
                100,
                anchor=N,
                font=('Purisa', 30),
                text='Ammo: {0}/10'.format(10 - maxshots))
            reload_done = True
            canvas.delete(reloadtxt)
        else:
            game.after(2000, self.reload)

    def __init__(  # Initializes the player and the keybinds for him
            self,
            x,
            y,
            r,
            image,
    ):
        global canvas
        gamesprite.__init__(self, x, y, r, image)
        self.direction = 'down'
        self.velocity = 0
        canvas.bind('<space>', self.shoot)
        canvas.bind('<r>', self.reload_timer)
        canvas.bind('<R>', self.reload_timer)
        canvas.bind('<KeyPress>', self.keypressed)
        canvas.bind('<KeyRelease>', self.keyreleased)
        canvas.focus_set()

    def movePlayer(self):  # Moves the player
        if self.direction == 'left':
            self.move(-self.velocity, 0)
            self.image_config(image=playerleft)
        elif self.direction == 'right':
            self.move(+self.velocity, 0)
            self.image_config(image=playerright)
        elif self.direction == 'up':
            self.move(0, -self.velocity)
            self.image_config(image=playerup)
        elif self.direction == 'down':
            self.move(0, +self.velocity)
            self.image_config(image=playerdown)
        self.border()

    def keypressed(self, event):  # Checks if the moving keys are pressed
        if event.char == 'a' or event.char == 'A':
            self.direction = 'left'
        elif event.char == 'd' or event.char == 'D':
            self.direction = 'right'
        elif event.char == 'w' or event.char == 'W':
            self.direction = 'up'
        elif event.char == 's' or event.char == 'S':
            self.direction = 'down'
        if event.char in [
                'w',
                'a',
                's',
                'd',
                'W',
                'A',
                'S',
                'D',
        ]:
            self.velocity = 8

    def keyreleased(self, event):  # And checks when they are released
        self.velocity = 0


def game_window(wsize, hsize):  # This function defines the main window
    game.title('Zombie Rush Invasion')
    global widthscreen
    global heightscreen
    widthscreen = game.winfo_screenwidth()
    heightscreen = game.winfo_screenheight()
    xvar = widthscreen / 2 - wsize / 2
    yvar = heightscreen / 2 - hsize / 2
    game.geometry('%dx%d+%d+%d' % (wsize, hsize, xvar, yvar))
    return game


def makeFullscreen():  # This function makes the game fullscreen
    game.attributes('-fullscreen', False)  # To swith press F11
    game.bind(
        '<F11>',
        lambda event: game.attributes('-fullscreen',
                                      not game.attributes('-fullscreen'))
    )


def pause(event):  # Main function for pausing the game
    global gamePaused
    global pausetxt
    global canvas
    global end
    global menu
    global countdown

    if not end:  # Checks if the game is already paused or if the game is over
        if gamePaused and countdown is False:
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
        elif not gamePaused and countdown is False:
            game_timer.pause()
            pausetxt = canvas.create_text(
                width // 2,
                height // 1.5,
                anchor=N,
                font=('Purisa', 40),
                text='Game Paused')
            gamePaused = not gamePaused


def ready_timer(
        time, text):  # Function that has a timer for when the game is unpaused
    global gamePaused
    global canvas
    global scoretxt
    global ammotxt
    global countdown
    if time > 0:
        if text is not None:
            canvas.delete(text)
        text = canvas.create_text(
            width // 2,
            height // 1.5,
            anchor=N,
            font=('Purisa', 40),
            text='Game resuimg in ' + str(time) + ' ...')
        game.after(500, lambda tr=time - 1, txt=text: ready_timer(tr, txt))
    else:
        canvas.delete(text)
        gamePaused = not gamePaused
        game_timer.unpause()
        for oneenemy in Enemy:
            oneenemy.start()
        canvas.delete(scoretxt)
        canvas.delete(ammotxt)
        scoretxt = canvas.create_text(
            150,
            50,
            anchor=N,
            font=('Purisa', 30),
            text='Score: ' + str(int(score)))
        ammotxt = canvas.create_text(
            175,
            100,
            anchor=N,
            font=('Purisa', 30),
            text='Ammo: {0}/10'.format(10 - maxshots))
        countdown = False


def game_loop(
):  # The main function for the game loop/game engine
    # which repeats for the game to run, in which all the actions happen
    global end
    global width
    global height
    global timertxt
    global scoretxt
    global maxshots
    global endtxt

    if end is False and gamePaused is False:
        Player.movePlayer()
        try:
            canvas.delete(timertxt)
        except NameError:
            pass
        timertxt = canvas.create_text(
            width - 200,
            height / 16,
            anchor=N,
            font=('Purisa', 30),
            text='Time left: ' + str(int(game_timer.get_time())))

        if int(game_timer.get_time()) == 0:
            end = True
            endtxt = canvas.create_text(
                width // 2,
                height // 1.5,
                anchor=N,
                font=('Purisa', 30),
                text='Time is up! You killed ' + str(score) + ' zombies')
            Player.change_coords(width // 2, height // 2)
            for oneenemy in Enemy:
                oneenemy.delete()
            dump_leaderboard()
            restart_vars()
            mainmenu()

        random_time = random.randint(200, 500)
        game.update()
        time.sleep(.001)

        height = canvas.winfo_height()
        width = canvas.winfo_width()
    else:

        for oneenemy in Enemy:
            oneenemy.stop()

    game.after(20, game_loop)


def random_enemy(
):  # Function to make sure that the enemis
    # are not spawned directly on the player
    global canvas
    global Player
    enemy_width = random.randint(0, width)
    enemy_height = random.randint(0, height)
    localplayer_coords = canvas.coords(Player.shape)
    while (enemy_width > localplayer_coords[0] - 160 and
            enemy_width < localplayer_coords[2] + 160 and
            enemy_height > localplayer_coords[1] - 160 and
            enemy_height < localplayer_coords[3] + 160):
        enemy_width = random.randint(100, width - 100)
        enemy_height = random.randint(100, height - 100)
    return (enemy_width, enemy_height)


def pausemenu_key(event):  # Event function to pause the game
    global gamePaused
    global end
    if not end:
        if not gamePaused:
            pause(None)
            pausemenu()


def unpausemenu_key(event):  # Event function to unpause the game
    global menu
    if not end:
        if gamePaused:
            pause(None)
            menu.destroy()


def pausemenu():  # Function that creates the pause menu
    global menu
    menu = menusettings()
    menu.bind('<Escape>', unpausemenu_key)
    Label(
        menu,
        text='Zombie Rush Invasion',
        bg='green',
        fg='darkred',
        font=('Purisa', 16, 'bold')).pack()
    Button(
        menu,
        text='Resume Game',
        command=lambda: pause(None),
        activeforeground='darkred',
        fg='darkred',
        activebackground='darkgreen',
        background='green',
        font=('Purisa', 13, 'bold'),
        pady=4,
    ).pack()
    Button(
        menu,
        text='Restart Game',
        command=lambda: restart_game(),
        activeforeground='darkred',
        fg='darkred',
        activebackground='darkgreen',
        background='green',
        font=('Purisa', 13, 'bold'),
        pady=4,
    ).pack()
    Button(
        menu,
        text='Enter/Change Username',
        command=lambda: input_user(),
        activeforeground='darkred',
        fg='darkred',
        activebackground='darkgreen',
        background='green',
        font=('Purisa', 11, 'bold'),
        pady=3,
    ).pack()
    Button(
        menu,
        text='Save Game',
        command=lambda: save_game(),
        activeforeground='darkred',
        fg='darkred',
        activebackground='darkgreen',
        background='green',
        font=('Purisa', 11, 'bold'),
        pady=3,
    ).pack()
    Button(
        menu,
        text='Load Game',
        command=lambda: load_game(),
        activeforeground='darkred',
        fg='darkred',
        activebackground='darkgreen',
        background='green',
        font=('Purisa', 11, 'bold'),
        pady=3,
    ).pack()
    Button(
        menu,
        text='Leaderboard',
        command=lambda: show_leaderboard(),
        activeforeground='darkred',
        fg='darkred',
        activebackground='darkgreen',
        background='green',
        font=('Purisa', 11, 'bold'),
        pady=3,
    ).pack()
    Button(
        menu,
        text='Exit',
        command=lambda: exit(),
        activeforeground='darkred',
        fg='darkred',
        activebackground='darkgreen',
        background='green',
        font=('Purisa', 12, 'bold'),
        pady=4,
    ).pack()
    Label(
        menu,
        text='W,A,S,D-Move, Space-Shoot R-Reload',
        bg='green',
        fg='darkred',
        font=('Purisa', 10, 'bold')).pack()
    Label(
        menu,
        text='Esc-Menu P-Pause F11-Fullscreen',
        bg='green',
        fg='darkred',
        font=('Purisa', 10, 'bold')).pack()
    Label(
        menu,
        text='time/score-cheatcodes, b-Bosskey',
        bg='green',
        fg='darkred',
        font=('Purisa', 10, 'bold')).pack()
    Label(
        menu,
        text=('To access a save file you must use the same \n'
              ' username with which the save file was made'),
        bg='green',
        fg='darkred',
        font=('Purisa', 10, 'bold')).pack()


def restart_game():  # Function that restarts the game
    global Enemy
    for oneenemy in Enemy:
        oneenemy.delete()
    restart_vars()
    reset_game()


def restart_vars(
):  # Function that resets all the variables for when the game is over
    global score
    global maxshots
    global game_timer
    global extra_zombies
    score = 0
    maxshots = 0
    extra_zombies = 0
    game_timer.reinit()
    game_timer.pause()


def reset_game():  # Function that starts/restarts the game
    global menu
    global Player
    global score
    global maxshots
    global gamePaused
    global Bullets
    global end
    global Enemy
    global ammotxt
    global scoretxt
    global pausetxt
    global extra_zombies

    try:
        canvas.delete(ammotxt)
        canvas.delete(scoretxt)
        canvas.delete(endtxt)
    except NameError:
        pass
    try:
        canvas.delete(pausetxt)
    except NameError:
        pass

    ammotxt = canvas.create_text(
        175,
        100,
        anchor=N,
        font=('Purisa', 30),
        text='Ammo: {0}/10'.format(10 - maxshots))
    scoretxt = canvas.create_text(
        150,
        50,
        anchor=N,
        font=('Purisa', 30),
        text='Score: ' + str(int(score)))
    for onebullet in Bullets:
        onebullet.delete()
    Player.change_coords(width // 2, height // 2)
    Enemy.clear()
    Bullets.clear()
    for _ in range(zombie_nr):
        coords = random_enemy()
        Enemy.append(makeEnemy(coords[0], coords[1], 50, enemyup))
    for _ in range(extra_zombies):
        coords = random_enemy()
        Enemy.append(makeEnemy(coords[0], coords[1], 50, enemyup))
    extra_zombies = 0
    menu.destroy()
    end = False
    pause(None)


def mainmenu():  # Function that creates the main menu
    global menu
    global gamePaused
    global game
    global end
    end = True
    gamePaused = True
    menu = menusettings()
    Label(
        menu,
        text='Zombie Rush Invasion',
        bg='green',
        fg='darkred',
        font=('Purisa', 16, 'bold')).pack()
    Label(
        menu,
        text=('Kill as many zombies within the time \n'
              ' 1 additional second for each zombie kill'),
        bg='green',
        fg='darkred',
        font=('Purisa', 10, 'bold')).pack()
    Button(
        menu,
        text='Start Game',
        command=lambda: reset_game(),
        activeforeground='darkred',
        fg='darkred',
        activebackground='darkgreen',
        background='green',
        font=('Purisa', 16, 'bold'),
        pady=7,
    ).pack()
    Button(
        menu,
        text='Enter/Change Username',
        command=lambda: input_user(),
        activeforeground='darkred',
        fg='darkred',
        activebackground='darkgreen',
        background='green',
        font=('Purisa', 11, 'bold'),
        pady=3,
    ).pack()
    Button(
        menu,
        text='Load Game',
        command=lambda: load_game(),
        activeforeground='darkred',
        fg='darkred',
        activebackground='darkgreen',
        background='green',
        font=('Purisa', 11, 'bold'),
        pady=3,
    ).pack()
    Button(
        menu,
        text='Leaderboard',
        command=lambda: show_leaderboard(),
        activeforeground='darkred',
        fg='darkred',
        activebackground='darkgreen',
        background='green',
        font=('Purisa', 11, 'bold'),
        pady=3,
    ).pack()
    Button(
        menu,
        text='Exit',
        command=lambda: exit(),
        activeforeground='darkred',
        fg='darkred',
        activebackground='darkgreen',
        background='green',
        font=('Purisa', 14, 'bold'),
        pady=5,
    ).pack()
    Label(
        menu,
        text='W,A,S,D-Move, Space-Shoot R-Reload',
        bg='green',
        fg='darkred',
        font=('Purisa', 10, 'bold')).pack()
    Label(
        menu,
        text='Esc-Menu P-Pause F11-Fullscreen',
        bg='green',
        fg='darkred',
        font=('Purisa', 10, 'bold')).pack()
    Label(
        menu,
        text='time/score-cheatcodes, b-Bosskey',
        bg='green',
        fg='darkred',
        font=('Purisa', 10, 'bold')).pack()
    Label(
        menu,
        text=('To access a save file you must use the same \n'
              ' username with which the save file was made'),
        bg='green',
        fg='darkred',
        font=('Purisa', 10, 'bold')).pack()


def input_user(
):  # Function that creats the menu in which the user enters his username
    global menu
    global user_menu
    global game
    global username
    menu.destroy()
    user_menu = Toplevel(game, bg='green', relief='ridge', bd=10)
    user_menu.wm_attributes('-type', 'splash')
    user_menu.grab_set()
    user_menu.focus_force()
    user_menu.transient(game)
    user_menu.geometry('300x180+{0}+{1}'.format(width // 2 - 150,
                                                height // 2 - 90 - 100))
    name = StringVar()
    Label(
        user_menu,
        text='Input your name below',
        bg='green',
        fg='darkred',
        font=('Purisa', 10, 'bold')).pack()
    Entry(user_menu, textvariable=name).pack()
    Button(
        user_menu,
        text='OK',
        command=lambda value=name: name_change(value),
        activeforeground='darkred',
        fg='darkred',
        activebackground='darkgreen',
        background='green',
        font=('Purisa', 14, 'bold'),
        pady=5,
    ).pack()
    Button(
        user_menu,
        text='Back',
        command=lambda menu=user_menu: backtomain(menu),
        activeforeground='darkred',
        fg='darkred',
        activebackground='darkgreen',
        background='green',
        font=('Purisa', 12, 'bold'),
        pady=4,
    ).pack()


def name_change(value):  # Function that gets the username and updates it
    global username
    global user_menu
    username = value.get()
    backtomain(user_menu)


def backtomain(menu):  # Function that goes back to the main menu or pause menu
    menu.destroy()
    if end:
        mainmenu()
    else:
        pausemenu()


def menusettings():  # Function that sets the settings for the menus
    menu = Toplevel(game, bg='green', relief='ridge', bd=10)

    # menu.attributes("-topmost", True)

    menu.wm_attributes('-type', 'splash')
    menu.grab_set()
    menu.focus_force()
    menu.transient(game)
    menu.geometry('400x460+{0}+{1}'.format(widthscreen // 2 - 200,
                                           heightscreen // 2 - 230 - 100))
    return menu


def save_game(
):  # Function that saves the game files and all the important variables
    global score
    global game_timer
    global maxshots
    global username
    global extra_zombies
    save_list = []
    save_list.append(score)
    save_list.append(game_timer)
    save_list.append(maxshots)
    save_list.append(extra_zombies)
    pickle.dump(save_list,
                open('savefiles/save_game_{0}.pkl'.format(username), 'wb'))


def load_game():  # Function that loads a save game file into the game
    global score
    global scoretxt
    global timertxt
    global game_timer
    global maxshots
    global username
    global Bullets
    global extra_zombies
    global zombie_nr
    try:
        load_list = pickle.load(
            open('savefiles/save_game_{0}.pkl'.format(username), 'rb'))
        score = load_list[0]
        game_timer = load_list[1]
        maxshots = load_list[2]
        extra_zombies = load_list[3]
        for onebullet in Bullets:
            onebullet.delete()
        Player.change_coords(width // 2, height // 2)
        for oneenemy in Enemy:
            coords = random_enemy()
            oneenemy.change_coords(coords[0], coords[1])
        if end is False:
            for one in Enemy:
                one.delete()
            Enemy.clear()
            for _ in range(zombie_nr):
                coords = random_enemy()
                Enemy.append(makeEnemy(coords[0], coords[1], 50, enemyup))
            for _ in range(extra_zombies):
                coords = random_enemy()
                Enemy.append(makeEnemy(coords[0], coords[1], 50, enemyup))
    except FileNotFoundError:

        pass


def show_leaderboard():  # Function that displays the leaderboard
    global menu
    global leader_menu
    global leaderboard
    global game
    leaderboard = pickle.load(open('Leaderboard.pkl', 'rb'))
    menu.destroy()
    leader_menu = Toplevel(game, bg='green', relief='ridge', bd=10)
    leader_menu.wm_attributes('-type', 'splash')
    leader_menu.grab_set()
    leader_menu.focus_force()
    leader_menu.transient(game)
    leader_menu.geometry('300x500+{0}+{1}'.format(width // 2 - 150,
                                                  height // 2 - 250 - 80))
    Button(
        leader_menu,
        text='Back',
        command=lambda menu=leader_menu: backtomain(menu),
        activeforeground='darkred',
        fg='darkred',
        activebackground='darkgreen',
        background='green',
        font=('Purisa', 12, 'bold'),
        pady=4,
    ).pack()
    for (key, var) in leaderboard.items():
        Label(
            leader_menu,
            text='Score {1} from {0}'.format(key, var),
            bg='green',
            fg='darkred',
            font=('Purisa', 12, 'bold')).pack()


def dump_leaderboard():  # Function that saves the score when the game is over
    global leaderboard
    global username
    if username is not None:
        leaderboard[username] = score
        leaderboard = dict(
            sorted(leaderboard.items(), key=lambda x: x[1], reverse=True))
        pickle.dump(leaderboard, open('Leaderboard.pkl', 'wb'))


def bosskey(event):  # Event function for the bosskey
    global boss_menu
    global gamePaused
    global widthscreen
    global heightscreen
    pause(None)
    boss_menu = Toplevel()
    boss_menu.attributes('-topmost', True)
    boss_menu.attributes('-fullscreen', True)
    boss_menu.attributes('-type', 'splash')
    boss_menu.bind('b', bossleft)
    boss_menu.bind('B', bossleft)
    boss_menu.focus_set()
    boss_canvas = Canvas(boss_menu)
    boss_canvas.create_image(widthscreen // 2, heightscreen // 2,
                             image=bossimg, anchor=CENTER)
    boss_canvas.pack(fill='both', expand=True)
    gamePaused = True


def bossleft(event):  # Event function for when you want to close the boss key
    global boss_menu
    pause(None)
    boss_menu.destroy()


def cheattime(event):  # Cheat for time
    global timer
    game_timer.timer = game_timer.timer + 100


def cheatscore(event):  # Cheat for score
    global canvas
    global score
    global scoretxt
    score = score + 50
    canvas.delete(scoretxt)
    scoretxt = canvas.create_text(
        150,
        50,
        anchor=N,
        font=('Purisa', 30),
        text='Score: ' + str(int(score)))


game = Tk()  # Initializing the window
global widthscreen
global heightscreen
global width
global height
widthscreen = game.winfo_screenwidth()
heightscreen = game.winfo_screenheight()
width = widthscreen
height = heightscreen

game = game_window(width, height)
canvas = Canvas(
    game, bg='darkgreen', relief='ridge',
    bd=20)  # Initializing the canvas on the window
canvas.pack(fill='both', expand=True)

makeFullscreen()

# All the images used below

bossimg = PhotoImage(file='images/bossimage.png')

imgup = PhotoImage(file='images/playerup.png')
playerup = imgup.subsample(3, 3)
imgdown = PhotoImage(file='images/playerdown.png')
playerdown = imgdown.subsample(3, 3)
imgleft = PhotoImage(file='images/playerleft.png')
playerleft = imgleft.subsample(3, 3)
imgright = PhotoImage(file='images/playerright.png')
playerright = imgright.subsample(3, 3)

eimgup = PhotoImage(file='images/enemyup.png')
enemyup = eimgup.subsample(2, 2)
eimgdown = PhotoImage(file='images/enemydown.png')
enemydown = eimgdown.subsample(2, 2)
eimgleft = PhotoImage(file='images/enemyleft.png')
enemyleft = eimgleft.subsample(2, 2)
eimgright = PhotoImage(file='images/enemyright.png')
enemyright = eimgright.subsample(2, 2)

bimgup = PhotoImage(file='images/bulletup.png')
bulletup = bimgup.subsample(4, 4)
bimgdown = PhotoImage(file='images/bulletdown.png')
bulletdown = bimgdown.subsample(4, 4)
bimgleft = PhotoImage(file='images/bulletleft.png')
bulletleft = bimgleft.subsample(4, 4)
bimgright = PhotoImage(file='images/bulletright.png')
bulletright = bimgright.subsample(4, 4)

# All the binds appart from the player ones

game.bind('<p>', pause)
game.bind('<P>', pause)
game.bind('<Escape>', pausemenu_key)
game.bind('time', cheattime)
game.bind('score', cheatscore)
game.bind('b', bosskey)
game.bind('B', bosskey)

global gamePaused
global end
global score
global maxshots
global reload_done
global Player
global Enemy
global countdown
global game_timer
global extra_zombies

try:  # Tries creating a leaderboard folder if it is not found
    leaderboard = pickle.load(open('Leaderboard.pkl', 'rb'))
except FileNotFoundError:
    leaderboard = {}

# Initializes all the variables when the programme is ran

score = 0
zombie_nr = 4
maxshots = 0
gamePaused = False
end = False
reload_done = True
username = None
countdown = False
extra_zombies = 0
game_timer = Clock()
game_timer.pause()

Enemy = list()
Bullets = list()

Player = makePlayer(width / 2, height / 2, 45, playerdown)

mainmenu()
game_loop()
game.mainloop()
