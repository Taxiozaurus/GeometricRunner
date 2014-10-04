# creator: Alexey "Taxiozaurus" Makeev
#
# Iceland, Reykjavik. Taekniskolinn - Upplysingataekniskolinn
#
# start of development: 17 Sep 2014
# this program/game is a project for school and is in under no means planned for further development after release
# all contributions via GitHub will still be accepted
# software/script is not copyrighted but when used please reference its original creator if used for demonstrations
#
# Quickly about this game:
# Have you heard of "impossible game"? if yes, you know what this is.
# game is about player getting from a beginning of a side-scrolling level to the end by jumping
# from pad/floor/panel/column to another and not smashing into walls/spikes and not falling down from the world

# all data will be defined in order of:
# imports,
# global variables,
# scoped variables,
# assets,
# external class initiation,
# functions/methods,
# game loop.
# this way code will be cleaner and easier to manage

import sys
import pygame
import random
import level
import scoreBoard
import keyLogger

from pygame.locals import *

pygame.init()

window = pygame.display.set_mode((800, 480))
pygame.display.set_caption('Geometric Run')

frameRate = pygame.time.Clock()

# define global here, they are required for ome elements to function properly
global click, frame, user, nick, password # external definition of some variables that need to be passed freely everywhere

# variables that have to stay same in between multiple frames
mousex, mousey, click, last_click, menuOffset, levelOffset, hiScore = 0, 0, False, False, 0, 0, 0
gravity, jumpForce, onGround, inJump = 0, 0, False, False
nick, password, user = "", "", -1
user_field_in_focus = False
pass_field_in_focus = False

GREEN =     (0, 255, 0) # define basic colors for further use with text
RED =       (255, 0, 0)
BLUE =      (0, 0, 255)
YELLOW =    (255, 255, 0)
PURPLE =    (100, 0, 200)

Wall =        pygame.Rect((0, 0), (60, 60)) # load assets
bgm =         pygame.image.load("assets/background.png")
SpikeUp =     pygame.image.load("assets/spikeUp.png") # string to a spiked 60px image here
SpikeLf =     pygame.image.load("assets/spikeLf.png")
SpikeDw =     pygame.image.load("assets/spikeDw.png")
SpikeRt =     pygame.image.load("assets/spikeRt.png")
SpikeSm =     pygame.image.load("assets/spikeSm.png")
WallBr =      pygame.image.load("assets/wallBr.png") # walls, BRick and HaZard
WallHz =      pygame.image.load("assets/wallHz.png")
plato =       pygame.image.load("assets/plato.png") # a thin surface
pad =         pygame.image.load("assets/pad.png")   # launches player 2 times as high as normal jump does

# fonts
robN = pygame.font.Font('assets/robotoNormal.ttf', 30)
robC = pygame.font.Font('assets/robotoCondens.ttf', 14)

# background location and definition to get seamless experience as it is made of 2 images that are made to overlap with each other
bgLoc1 = 0
bgLoc2 = 800

# random background color because image is transparent and game is kinda colourful, at least it is supposed to be
bgCol = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))

# set up usage of level loading class
Levels = level.Level()
Scores = scoreBoard.Score()
Username = keyLogger.KeyLogger(300, 20)
Password = keyLogger.KeyLogger(300, 20)

# get headers and info for levels as well as levels themselves
levelHead, g = Levels.loadLevels()

# Level rendering and execution as well as "frames" management, every menu item here will be represented as "frame" for game window
# this is made so management of gameplay attributes would be easier to call and debug
frame = 0


########################################################################################################################
#####################################################      LogIn     ###################################################
def log_in() :
    global user_field_in_focus, pass_field_in_focus, user, password, nick, frame

    userfield = pygame.Rect((250, 140), (300, 20))
    passfield = pygame.Rect((250, 180), (300, 20))

    pygame.draw.rect(window, PURPLE, userfield)
    pygame.draw.rect(window, PURPLE, passfield)

    if click :
        user_field_in_focus = False
        pass_field_in_focus = False

    if userfield.collidepoint(mousex, mousey) and click :
        user_field_in_focus = True
    if passfield.collidepoint(mousex, mousey) and click :
        pass_field_in_focus = True


    if user_field_in_focus :
        nick, user_surface = Username.getinput()
        window.blit(user_surface, userfield)
    if pass_field_in_focus :
        password, password_surface = Password.getinput()
        window.blit(password_surface, passfield)

    log_in_base = pygame.Rect((320, 250), (160, 80))
    pygame.draw.rect(window, PURPLE, log_in_base)

    log_in_button = robN.render("LogIn", True, YELLOW, PURPLE)
    log_in_rect = log_in_button.get_rect()
    log_in_rect.center = log_in_base.center

    window.blit(log_in_button, log_in_rect)

    if log_in_base.collidepoint(mousex, mousey) and click :
        user = Scores.login(nick, password)
        if user != "" :
            frame = 1

########################################################################################################################
######################################################      Menu     ###################################################
def main_menu() :
    global frame
    button1 = pygame.Rect((310, 200), (220, 120))
    pygame.draw.rect(window, PURPLE, button1)
    text_surface = robN.render("Play", True, YELLOW, PURPLE)
    button_text_rect = text_surface.get_rect()
    button_text_rect.center = (410, 270)
    window.blit(text_surface, button_text_rect) # A BIG F***ING PLAY BUTTON

    if button1.collidepoint(mousex, mousey) and click :
        frame = 2


########################################################################################################################
##################################################      Level Select    ################################################
def select_level() : # loads and shows a list of levels and arrow buttons to navigate level selection
    global menuOffset, frame
    pos1, pos2 = 400, 200 # button offsets in x/y grid
    cctn = 0
    for i in levelHead :
        cctn += 1 # for loop gives back an array (i) from the 2D levelHead array, thus external integer is required for count
        selector = pygame.Rect((pos1 * cctn - (100 + menuOffset * 400), pos2), (200, 120))
        z = "" # level names in levels.txt file are written with ## prefix, string is reformatted here
        c = 0
        for a in i[0] :
            if c > 1 :
                z += a
            c += 1

        level_name = robN.render(z, True, YELLOW, PURPLE) # level selector button
        pygame.draw.rect(window, PURPLE, selector)
        window.blit(level_name, (pos1 * cctn - (50 + menuOffset * 400), pos2 + 20)) # level "icon"
        if selector.collidepoint(mousex, mousey) and click :
            frame = 3

    # menuOffset triggers (e.g. left/right buttons for level select
    if menuOffset > 0 :
        menu_left = pygame.Rect((200, 210), (50, 100))
        pygame.draw.polygon(window, BLUE, ((250, 210), (250, 310), (200, 260)))
        if menu_left.collidepoint(mousex,mousey) and click :
            menuOffset -= 1
            print menuOffset
    if menuOffset < len(g) - 1 :
        menu_right = pygame.Rect((550, 210), (50, 100))
        pygame.draw.polygon(window, BLUE, ((550, 210), (550, 310), (600, 260)))
        if menu_right.collidepoint(mousex, mousey) and click :
            menuOffset += 1
            print menuOffset

    menu = robC.render("Menu", True, YELLOW, PURPLE) # return to menu button
    mect = menu.get_rect()
    mect.center = (70, 25)
    window.blit(menu, mect)
    if mect.collidepoint(mousex, mousey) and click :
        frame = 1


########################################################################################################################
####################################################      Player     ###################################################
def player_died() : # this function is a sequence that will be triggered every time player smashes into something (fails)
    global hiScore, levelOffset, gravity, jumpForce, inJump, onGround
    if hiScore < len(g[menuOffset][0]) * 60 / levelOffset : # check hi-score
            hiScore = len(g[menuOffset][0]) * 60 / levelOffset # apply new value

    # reset variables
    levelOffset = 0
    gravity = 0
    jumpForce = 0
    inJump = False
    onGround = False


def player_movement(walls, spikes, jump_pads) :
    global levelOffset, gravity, onGround, hiScore, jumpForce, inJump, initJump
    player_y = 300

    if click and onGround : #jump action
        inJump = True
        jumpForce = 15
        initJump = 15
        onGround = False

    if inJump : # jump is separated from gravity as gravity will override proper sequence of acceleration
        jumpForce = jumpForce + initJump - 1
        initJump -= 1

    if not onGround and not inJump:
        gravity += 10

    player_pos_y = player_y + gravity - jumpForce

    player = pygame.Rect((120, player_pos_y), (60, 60)) # set up position of player
    #event/execute/collisionCheck/apply
    onGround = False
    for wall in walls :
        if 90 < wall.centerx < 210 and wall.top >= player.bottom : # if player is on ground
            if wall.top == player.bottom :
                onGround = True
                inJump = False

    spiked = player.collidelist(spikes) # determines if player has smashed into any of the spikes that are available in the level to reset
    if spiked >= 0 or player_pos_y > 900:
        player_died()

    pygame.draw.rect(window, PURPLE, player)


########################################################################################################################
#####################################################      Level     ###################################################
def run_level() : # uses global variables that were set in level selection to run desired level instead of them being passed by, this is because of implementing "frame" UI design
    walls = []
    jump_pads = []
    spikes = []
    global menuOffset, levelOffset, frame, hiScore
    levelOffset += 12
    selected_level = g[menuOffset]

    for a in range(0, len(selected_level[0])-1) : # levels must be with 1 extra column as to prevent from random a peculiar bug of "new line syndrome"
                                        # this but is in the mean of last row of last level holds no "new line" or \n in it
                                        # and since len() method counts \n as a char, last line becomes shorter than first line in the last level
                                        # other solution may be of adding an extra character in the end of last line or adding next line
                                        # but these solutions are "hard-coded", thus useless
        for i in range(0, len(selected_level)) :
            # asset index: w h <^>v s j p .
            # wallNormal/wallHazard/spikeLeft/spikeUp/spikeRight/spikeDown/smallSpike/jumpPad/plato/empty
            # these if statements serve as a level generator by utilizing a 60x60 px grid

            h = pygame.Rect((60 * a - levelOffset, 60 * i), (60, 60))

            if selected_level[i][a] == 'h' :
                window.blit(WallHz, h)
                walls.append(h)
            elif selected_level[i][a] == 'w' :
                window.blit(WallBr, h)
                walls.append(h)
            elif selected_level[i][a] == '<' :
                sl = pygame.Rect((60 * a - levelOffset + 10, 60 * i + 20), (50, 20))
                window.blit(SpikeLf, h)
                spikes.append(sl)
            elif selected_level[i][a] == '^' :
                su = pygame.Rect((60 * a - levelOffset + 20, 60 * i + 10), (20, 50))
                window.blit(SpikeUp, h)
                spikes.append(su)
            elif selected_level[i][a] == '>' :
                sr = pygame.Rect((60 * a - levelOffset + 10, 60 * i), (50, 20))
                window.blit(SpikeRt, h)
                spikes.append(sr)
            elif selected_level[i][a] == 'v' :
                sd = pygame.Rect((60 * a - levelOffset + 20, 60 * i), (20, 50))
                window.blit(SpikeDw, h)
                spikes.append(sd)
            elif selected_level[i][a] == 's' :
                s = pygame.Rect((60 * a - levelOffset, 60 * i + 45), (60, 15))
                window.blit(SpikeSm, s)
                spikes.append(s)
            elif selected_level[i][a] == 'p' :
                p = pygame.Rect((60 * a - levelOffset, 60 * i), (60, 15))
                window.blit(plato, p)
                walls.append(p)
            elif selected_level[i][a] == 'j' :
                j = pygame.Rect((60 * a - levelOffset, 60 * i + 45), (60, 15))
                window.blit(pad, j)
                jump_pads.append(pad)

    player_movement(walls, spikes, jump_pads)

    exit_button = robC.render("Exit", True, YELLOW, PURPLE)
    exit_rect = exit_button.get_rect()
    exit_rect.center = (70, 25)
    window.blit(exit_button, exit_rect)

    if exit_rect.collidepoint(mousex, mousey) or levelOffset > (len(selected_level[0]) - 2) * 60 : # goto score or end of level
        if hiScore < len(g[menuOffset][0]) * 60 / levelOffset :
            hiScore = len(g[menuOffset][0]) * 60 / levelOffset
        frame = 4


########################################################################################################################
#####################################################      Score     ###################################################
def game_score() :
    global frame, hiScore, menuOffset


########################################################################################################################
##################################################      Game Loop     ##################################################
while True : # game loop
    click = False
    if not last_click :
        click = pygame.mouse.get_pressed()[0]

    mousex, mousey = pygame.mouse.get_pos()

    if click :
        last_click = True
        bgCol = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)) # get new bgcolor for every click

    # background movement mechanism, it is on constant movement to the left
    bgLoc1 -= 1
    bgLoc2 -= 1
    # if image is out of window on left side, it is moved back to the right so the "seamless" bg is visible
    if bgLoc1 == -800 :
        bgLoc1 = 800
    if bgLoc2 == -800 :
        bgLoc2 = 800
    window.fill(bgCol)
    window.blit(bgm, (bgLoc1, 0))
    window.blit(bgm, (bgLoc2, 0))

    # here ends the "preparation of the game base
    # background is on constant move and on every click its colour changes
    # colour change feature is designed to enhance game mechanics and design to add dynamics

    # every function represents its own elements and shows unique data to it
    # for instance mainMenu function introduces buttons that wil send player to level select menu or game hi-score
    # also this way debugging is easier
    if frame == 0:
        log_in()
    elif frame == 1 :
        main_menu()
    elif frame == 2 :
        select_level()
    elif frame == 3 :
        run_level()
    elif frame == 4 :
        game_score()

    for event in pygame.event.get() :
        if event.type == QUIT :
            pygame.quit()
            sys.exit()
        if event.type == MOUSEBUTTONUP :
            last_click = False

    pygame.display.update()
    frameRate.tick(30)