 #This is written by Ashley Christendat. This is the final ICS4U culminating game.
#This game is a two person racing game and it is called Sled Runners.
#This is started on November 24, 2021 and finished on January 19, 2022.

import pygame, os, random, time
from pygame.locals import *

# set up the window
WINDOWWIDTH = 1200
WINDOWHEIGHT = 800

# set up colours
BLUE = (148, 206, 255)

# set up other constants
FRAMERATE = 40
INITALFOOD = 3
NEWFOOD = 1
INITALBADFOOD = 1
NEWBADFOOD = 3
GAMELENGTH = 45

def terminate():
    """ This function is called when the user closes the window or presses ESC """
    pygame.quit()
    os._exit(1)

def load_image(filename):
    """ Load an image from a file.  Return the image and corresponding rectangle """
    image = pygame.image.load(filename)
    image = image.convert_alpha()   
    return image

def drawText(text, font, surface, x, y, textcolour):
    """ Draws the text on the surface at the location specified """
    textobj = font.render(text, 1, textcolour)
    textrect = textobj.get_rect()
    textrect.topleft = (x, y)
    surface.blit(textobj, textrect)

def menu_display(windowSurface):
    """ Display the main menu screen """
    # load the main menu image and blit it at (0,0)
    menu = load_image("mainmenu.png")
    windowSurface.blit(menu, (0,0))
    pygame.display.update()

def screen_display(image, windowSurface):
    """ Display a screen for 1 second"""
    windowSurface.blit(image, (0,0))
    pygame.display.update()
    time.sleep(1)

def choose_option(windowSurface):
    """Choose an option displayed on the menu screen"""
    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                terminate()
                
            # add buttons for each option on the main menu
            elif event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                # button for start
                if (pos[0] <= 712 and pos[0] >= 490) and (pos[1] <= 363 and pos[1] >= 303):
                    optionchosen = True
                    return optionchosen
                else:
                    # button for instructions
                    if (pos[0] <= 870 and pos[0] >= 380) and (pos[1] <= 516 and pos[1] >= 456):
                        image = load_image("objective.png")
                        optionchosen = input_two(windowSurface, image)

                        # load the second image for the instructions and go through the input_two function
                        image = load_image("controls.png")
                        optionchosen = input_two(windowSurface, image)
                        return optionchosen

                    # button for credits
                    elif (pos[0] <= 744 and pos[0] >= 462) and (pos[1] <= 670 and pos[1] >= 610):
                        image = load_image("creds.png")
                        optionchosen = input_two(windowSurface, image)
                        return optionchosen
                    
            # quit if player presses the escape key
            elif event.type == KEYUP:
                if event.key == K_ESCAPE:
                    terminate()

def input_two(windowSurface, image):
    """ Choose the option to go back to main menu screen """
    # blit the image loaded in the choose_option function
    windowSurface.blit(image, (0,0))
    pygame.display.update()
    
    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                terminate()

            # return to choose_option function if space is pressed
            elif event.type == KEYDOWN:
                if event.key == ord(' '):
                    return False
    
class Player(pygame.sprite.Sprite):
    """ Player that the user can move """
    def __init__(self, image, scale, x, y, points):
        # setting up player 
        pygame.sprite.Sprite.__init__(self)
        self.original = image
        self.image = pygame.transform.scale(image, scale)
        self.rect = self.image.get_rect()
        self.points = points

        self.rect.y = y
        self.rect.x = x

        self.change_x = 0
        self.change_y = 0

        self.wall_list = None

    def changespeed(self, x, y):
        """ Change the speed of the player """
        self.change_x += x
        self.change_y += y
        
    def update(self):
        """ Update the direction and place of the player. """
        
        self.rect.x += self.change_x

        # they player doesn't move past a barrier when the player collides 
        barrier_hit_list = pygame.sprite.spritecollide(self, self.wall_list, False)
        for barrier in barrier_hit_list:
            if self.change_x > 0:
                self.rect.right = barrier.rect.left
            else:
                self.rect.left = barrier.rect.right

        self.rect.y += self.change_y

        barrier_hit_list = pygame.sprite.spritecollide(self, self.wall_list, False)
        for barrier in barrier_hit_list:
            if self.change_y > 0:
                self.rect.bottom = barrier.rect.top
            else:
                self.rect.top = barrier.rect.bottom
                
class Food(pygame.sprite.Sprite):
    """ A piece of food to be eaten by the player """
    def __init__(self, image, movespeed):
        # setting up the food
        pygame.sprite.Sprite.__init__(self)
        self.original = image
        self.image = pygame.transform.scale(image, (40,40))
        self.rect = self.image.get_rect()
        self.movespeed = movespeed
        
        # set the position to a random place between 2 y coordinates
        self.rect.top = random.randrange(500, 760)
        self.rect.left = WINDOWWIDTH
        
    def update (self):
        """ update the location of the food """
        # move the food to the left
        self.rect.left -= self.movespeed
        
        # kill the food once it reaches the other side
        if self.rect.left < 0:
            self.kill()

class Finish_Line(pygame.sprite.Sprite):
    """ A finish line to move across the screen """
    def __init__(self, image):
        # setting up the finish line
        pygame.sprite.Sprite.__init__(self)
        self.image = image
        self.rect = self.image.get_rect()
        
        self.rect.top = 523
        self.rect.left = 1195
        
    def update (self):
        """ update the location of the food """
        # move the line 3 blocks to the left
        self.rect.left -= 3

class Barrier(pygame.sprite.Sprite):
    """ Barrier that the player cannot move across """
    def __init__ (self, x, y, width, height):
        # setting up the barrier
        pygame.sprite.Sprite.__init__(self)

        self.original = load_image("transparent.png")
        self.image = pygame.transform.scale(self.original, (width,height))

        self.rect = self.image.get_rect()
        self.rect.y = y
        self.rect.x = x

class Background(pygame.sprite.Sprite):
    """ background that moves """
    def __init__ (self, image):
        # setting up the background image that moves from right to left
        self.image = image
        self.rect = self.image.get_rect()

        # creating two rectangles with the same image and moving both of them
        self.Y1 = 0
        self.X1 = 0

        self.Y2 = 0
        self.X2 = WINDOWWIDTH

    def update(self):
        # move the background 3 blocks to the left
        self.X1 -= 3
        self.X2 -= 3

        # if one rectangle moves to the end of the window, make it's x coordinate the width of the window
        if self.X1 <= -self.rect.width:
            self.X1 = self.rect.width
        if self.X2 <= -self.rect.width:
            self.X2 = self.rect.width

    def render(self, windowSurface):
        # blit both of the images
        windowSurface.blit(self.image, (self.X1, self.Y1))
        windowSurface.blit(self.image, (self.X2, self.Y2))

class Game(pygame.sprite.Sprite):
    """ control all the game functions, can restart """
    def __init__(self):
        # set to true after a certain amount of time
        self.game_over = False

        # set to true once game is over and player wants to restart
        self.restart = False

        # set to true once finish line appears
        self.finishing = False
        
        # set up the player, wall and food groups
        self.all_sprites = pygame.sprite.Group()
        self.foods = pygame.sprite.Group()
        self.wall_list = pygame.sprite.Group()
        self.all_players = pygame.sprite.Group()
        self.badfoods = pygame.sprite.Group()

        # loading all the images
        self.forest = load_image("forest.png")

        self.ending = load_image("endingscreen.png")
        self.tie = load_image("tie.png")
        self.winner1 = load_image("1.png")
        self.winner2 = load_image("2.png")

        self.fline = load_image("finishline.png")
        
        self.present = load_image("present.png")
        self.candycane = load_image("candycane.png")
        self.bauble = load_image("bauble.png")
        self.gingerbreadman = load_image("gingerbreadman.png")
        self.christmastree = load_image("christmastree1.png")
        self.stocking = load_image("stocking.png")

        self.grinch = load_image("grinch.png")
        self.coal = load_image("coal.png")

        sleigh1 = load_image("sleigh.png")
        sleigh2 = load_image("sleigh2.png")

        # setting up two lists with the 'good' and 'bad' food images
        self.ranfoodlist = [self.present, self.candycane, self.bauble, self.gingerbreadman, self.christmastree, self.stocking]
        self.ranbadfoodlist = [self.grinch, self.coal]

        # randomize which food appears
        for i in range(INITALBADFOOD):
            self.randnum = random.randrange(len(self.ranbadfoodlist))
            abadfood = Food(self.ranbadfoodlist[self.randnum], 4)
            self.badfoods.add(abadfood)
            self.all_sprites.add(abadfood)
            
        for i in range(INITALFOOD):
            self.randnum = random.randrange(len(self.ranfoodlist))
            afood = Food(self.ranfoodlist[self.randnum], 3)
            self.foods.add(afood)
            self.all_sprites.add(afood)
            
        # setting up the walls
        self.wall = Barrier(0, 480, 1200, 5)
        self.wall_list.add(self.wall)
        self.all_sprites.add(self.wall)

        self.wall = Barrier(0, 795, 1200, 5)
        self.wall_list.add(self.wall)
        self.all_sprites.add(self.wall)

        # setting up the finish line
        self.finishline = Finish_Line(self.fline)

        # setting up the background
        self.background = Background(self.forest)
        
        # setting up the players
        self.player1 = Player(sleigh1, (120,78), 100, 600, 0)
        self.player2 = Player(sleigh2, (120,95), 100, 650, 0)
        self.all_sprites.add(self.player1)
        self.all_sprites.add(self.player2)

        self.all_players.add(self.player1)
        self.all_players.add(self.player2)
        
        self.player1.wall_list = self.wall_list
        self.player2.wall_list = self.wall_list

        self.all_sprites.add(self.badfoods)
        self.all_sprites.add(self.foods)

        # setting up music
        self.pickUpSound = pygame.mixer.Sound('pickup.wav')
        self.badpickUpSound = pygame.mixer.Sound('badpickup.wav')
        pygame.mixer.music.load('background.mp3')
        pygame.mixer.music.set_volume(0.3)
        self.gameOverSound = pygame.mixer.Sound('gameover.wav')

        # play the background music
        pygame.mixer.music.play(-1, 0.0)
        self.musicPlaying = True
        
        # setting up the timers
        self.startfoodtime = time.time()
        self.startbadfoodtime = time.time()
        self.startgametime = time.time()

    def process_events(self, windowSurface):
        """ Respond to keyboard and mouse clicks"""
        for event in pygame.event.get():
            if event.type == QUIT:
                terminate()
            elif event.type == KEYDOWN:
                # update the direction of the players
                if event.key == ord('w'):
                    self.player1.changespeed(0, -5)
                elif event.key == ord('s'):
                    self.player1.changespeed(0, 5)

                elif event.key == pygame.K_UP:
                    self.player2.changespeed(0, -5)
                elif event.key == pygame.K_DOWN:
                    self.player2.changespeed(0, 5)

                elif event.key ==ord(' '):
                    # restart the game if player presses space and game is over
                    if self.game_over:
                        self.restart = True
                
            elif event.type == KEYUP:
                if event.key == K_ESCAPE:
                    terminate()
                    
                # make the player stop moving when the key is not pressed
                if event.key == ord('w'):
                    self.player1.changespeed(0, 5)
                elif event.key == ord('s'):
                    self.player1.changespeed(0, -5)

                elif event.key == pygame.K_UP:
                    self.player2.changespeed(0, 5)
                elif event.key == pygame.K_DOWN:
                    self.player2.changespeed(0, -5)
                elif event.key == ord('m'):
                    # toggles the background music
                    if self.musicPlaying:
                        pygame.mixer.music.stop()
                    else:
                        pygame.mixer.music.play(-1, 0.0)
                    self.musicPlaying = not self.musicPlaying
                    
    def run_logic(self):
        """ Check for collisions and new food """
        if not self.game_over:
            endfoodtime = time.time()
            endbadfoodtime = time.time()
            if not self.finishing:
                if endfoodtime - self.startfoodtime >= NEWFOOD:
                    # reset counter and add new 'good' food
                    self.startfoodtime = time.time()
                    self.randnum = random.randrange(len(self.ranfoodlist))
                    afood = Food(self.ranfoodlist[self.randnum], 3)
                    self.foods.add(afood)
                    self.all_sprites.add(afood)
                if endfoodtime - self.startbadfoodtime >= NEWBADFOOD:
                    # reset counter and add new food
                    self.startbadfoodtime = time.time()
                    self.randnum = random.randrange(len(self.ranbadfoodlist))
                    abadfood = Food(self.ranbadfoodlist[self.randnum], 4)
                    self.badfoods.add(abadfood)
                    self.all_sprites.add(abadfood)

            # adding points if there are any collisions         
            food_hit_list_1 = pygame.sprite.spritecollide(self.player1, self.foods, True)
            for afood in food_hit_list_1:
                self.player1.points += 1
            
            food_hit_list_2 = pygame.sprite.spritecollide(self.player2, self.foods, True)
            for afood in food_hit_list_2:
                self.player2.points += 1
                    
            # removing points if there are any collisions    
            badfood_hit_list_1 = pygame.sprite.spritecollide(self.player1, self.badfoods, True)
            for abadfood in badfood_hit_list_1:
                self.player1.points -= 2
                
            badfood_hit_list_2 = pygame.sprite.spritecollide(self.player2, self.badfoods, True)
            for abadfood in badfood_hit_list_2:
                self.player2.points -= 2

            # Play the pickup sound for each food eaten
            if self.musicPlaying:
                for afood in food_hit_list_1:
                    self.pickUpSound.play()

                for afood in food_hit_list_2:
                    self.pickUpSound.play()

                for afood in badfood_hit_list_1:
                    self.badpickUpSound.play()

                for afood in badfood_hit_list_2:
                    self.badpickUpSound.play()

            # setting up the time that will be displayed    
            currenttime = time.time() - self.startgametime
            self.displaytime = GAMELENGTH - currenttime
            if self.displaytime <= 0:
                # ending the game if the display time is less than or equal to 0 seconds
                self.game_over = True
                pygame.mixer.music.stop()
                if self.musicPlaying:
                    self.gameOverSound.play()

                # determining the winner
                if self.player1.points > self.player2.points:
                    self.winner = 1
                elif self.player1.points < self.player2.points:
                    self.winner = 2
                    
                else:
                    self.winner = 0
                    
            # if there are about 9 seconds left
            elif int(self.displaytime) == 9:
                self.all_sprites.add(self.finishline)
                self.finishing = True

    def display_frame(self, windowSurface):
        """ Display all the sprites on the screen """
        if self.game_over:
            # draw different screens depending on the ending
            if self.winner != 0:
                windowSurface.blit(self.ending, (0,0))
                if self.winner == 1:
                    windowSurface.blit(self.winner1, (555, 500))
                else:
                    windowSurface.blit(self.winner2, (545, 500))

            elif self.player1.points == self.player2.points:
                windowSurface.blit(self.tie, (0,0))                
        # draw the window onto the screen
        else:
            # draw background to the screen
            self.background.render(windowSurface)
            self.background.update()

            # draw all the text to the screen
            basicFont = pygame.font.SysFont("Arial", 20, True)
            timetext = ['Time: ' + str(round(self.displaytime, 1)) + 's']
            for i in range(len(timetext)):
                drawText(timetext[i], basicFont, windowSurface, 50, 20, BLUE)
            
            point1text = ['Player 1 Points: ' + str(self.player1.points)]
            for i in range(len(point1text)):
                drawText(point1text[i], basicFont, windowSurface, 50, 50, BLUE)

            point2text = ['Player 2 Points: ' + str(self.player2.points)]
            for i in range(len(point2text)):
                drawText(point2text[i], basicFont, windowSurface, 250, 50, BLUE)
                
            # drawing all the sprites onto the window
            self.all_sprites.draw(windowSurface)
            self.all_players.draw(windowSurface)
        pygame.display.update()

def main():
    # set up pygame
    pygame.init()
    mainClock = pygame.time.Clock()
    #Set up the windowSurface
    windowSurface = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT), 0, 32)
    pygame.display.set_caption("Sled Runners")
    start3 = load_image('3start.png')
    start2 = load_image('2start.png')
    start1 = load_image('1start.png')
    go = load_image('go.png')

    while True:
        start = False
        # while loop to stay in the menu screens
        while start == False:
            menu_display(windowSurface)
            start = choose_option(windowSurface)

        screen_display(start3, windowSurface)
        screen_display(start2, windowSurface)
        screen_display(start1, windowSurface)
        screen_display(go, windowSurface)
        game = Game()

       # while loop to stay in the game
        while not game.restart:
            game.process_events(windowSurface)
            
            game.all_sprites.update()
            
            game.run_logic()
            
            game.display_frame(windowSurface)
            
            mainClock.tick(FRAMERATE)

main()
