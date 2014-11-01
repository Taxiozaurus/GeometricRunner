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
import math

from pygame.locals import *

pygame.init()

window = pygame.display.set_mode((800, 480))
pygame.display.set_caption('Geometric Run')

frameRate = pygame.time.Clock()

# define global here, they are required for ome elements to function properly
global click, frame, user, nick, password, levelSurface # external definition of some variables that need to be passed freely everywhere

# variables that have to stay same in between multiple frames
mousex, mousey, click, last_click, menuOffset, level_offset, vertical_offset, hiScore = 0, 0, False, False, 0, 0, 0, 0
gravity, jumpForce, prevForce, initJump, onGround, inJump, player_pos_y, player_rotation, oldJump = 0, 0, 0, 0, False, False, 240, False, 0
nick, password, user = "", "", -1
user_field_in_focus = False
pass_field_in_focus = False
walls, jump_pads, spikes, loaded, calledm, angle_state, old_angle = [], [], [], False, False, 0, 0

levelSurface = pygame.Surface((0, 0), SRCALPHA) # level rendering surface with alpha pixel value

GREEN =     (0, 255, 0) # define basic colors for further use with text
RED =       (255, 0, 0)
BLUE =      (0, 0, 255)
YELLOW =    (255, 255, 0)
PURPLE =    (100, 0, 200)

pygame.mixer.music.load('assets/menu.mp3') # background sound and audio output for levels and main menu
pygame.mixer.music.play(-1)

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
player =      pygame.image.load("assets/player.png")
playerSurface = pygame.Surface((60, 60), SRCALPHA) # create a surface entity that will handle rotation of player in jump
playerSurface.blit(player, (0, 0, 0, 0))

# fonts
robN = pygame.font.Font('assets/robotoNormal.ttf', 30)
robC = pygame.font.Font('assets/robotoCondens.ttf', 14)

# background location and definition to get seamless experience as it is made of 2 images that are made to overlap with each other
bgLoc1 = 0
bgLoc2 = 800

# random background color because image is transparent and game is kinda colourful, at least it is supposed to be
bgCol = (random.randint(60, 255), random.randint(60, 255), random.randint(60, 255))

# set up usage of level loading class
Levels = level.Level()
Scores = scoreBoard.Score()
Username = keyLogger.KeyLogger(300, 20, "username")
Password = keyLogger.KeyLogger(300, 20, "password")

# get headers and info for levels as well as levels themselves
levelHead, g = Levels.loadLevels()
# Level rendering and execution as well as "frames" management, every menu item here will be represented as "frame" for game window
# this is made so management of gameplay attributes would be easier to call and debug
frame = 0


########################################################################################################################
#####################################################      LogIn     ###################################################
def log_in() :
    global user_field_in_focus, pass_field_in_focus, user, password, nick, frame

    user_field = pygame.Rect((250, 140), (300, 20)) # placement of text fields for both username and password
    password_field = pygame.Rect((250, 180), (300, 20))

    pygame.draw.rect(window, PURPLE, user_field) # apply beforehand to secure proper focus selection
    pygame.draw.rect(window, PURPLE, password_field)

    if click : # text field de-select
        user_field_in_focus = False
        pass_field_in_focus = False

    if user_field.collidepoint(mousex, mousey) and click : # text field select
        user_field_in_focus = True
    if password_field.collidepoint(mousex, mousey) and click :
        pass_field_in_focus = True

    nick, user_surface = Username.get_input(user_field_in_focus) # gather data from keyLogger class
    password, password_surface = Password.get_input(pass_field_in_focus)

    window.blit(user_surface, user_field)
    window.blit(password_surface, password_field)

    log_in_base = pygame.Rect((320, 250), (160, 40))
    pygame.draw.rect(window, PURPLE, log_in_base)

    reg_base = pygame.Rect((360, 300), (80, 20))
    pygame.draw.rect(window, PURPLE, reg_base)

    log_in_button = robN.render("LogIn", True, YELLOW, PURPLE)
    log_in_rect = log_in_button.get_rect()
    log_in_rect.center = log_in_base.center

    reg_button = robC.render("Register", True, YELLOW, PURPLE)
    reg_rect = reg_button.get_rect()
    reg_rect.center = reg_base.center

    window.blit(log_in_button, log_in_rect)
    window.blit(reg_button, reg_rect)

    if log_in_base.collidepoint(mousex, mousey) and click :
        user = Scores.login(nick, password)
        if user != "" :
            frame = 1
    if reg_base.collidepoint(mousex, mousey) and click :
        user = Scores.register(nick, password)
        if user != "" :
            frame = 1


########################################################################################################################
######################################################      Menu     ###################################################
def main_menu() :
    global frame
    button1 = pygame.Rect((300, 150), (200, 120))
    pygame.draw.rect(window, PURPLE, button1)
    text_surface = robN.render("Play", True, YELLOW, PURPLE)
    button_text_rect = text_surface.get_rect()
    button_text_rect.center = (400, 210)
    window.blit(text_surface, button_text_rect) # A BIG F***ING PLAY BUTTON

    if button1.collidepoint(mousex, mousey) and click :
        frame = 2


########################################################################################################################
##################################################      Level Select    ################################################
def select_level() : # loads and shows a list of levels and arrow buttons to navigate level selection
    global menuOffset, frame, hiScore, loaded, called
    pos1, pos2 = 400, 150 # button offsets in x/y grid
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
        window.blit(level_name, (pos1 * cctn - (35 + menuOffset * 400), pos2 + 20)) # level "icon"
        if selector.collidepoint(mousex, mousey) and click :
            loaded = False # set level load to new
            called = False # set scoreboard to call new one
            asrc = ""
            for i in range(0, len(levelHead[menuOffset][2])) : # get rid of /n (newline) and # from string
                if 0 < i < len(levelHead[menuOffset][2]) - 1:
                    asrc += levelHead[menuOffset][2][i]
            if '/' in asrc : # apply song to mixer if path is valid
                pygame.mixer.music.load(asrc)
                pygame.mixer.music.play()
            hiScore = 0
            frame = 3

    # menuOffset triggers (e.g. left/right buttons for level select
    if menuOffset > 0 :
        menu_left = pygame.Rect((200, 160), (50, 100))
        pygame.draw.polygon(window, BLUE, ((250, 160), (250, 260), (200, 210)))
        if menu_left.collidepoint(mousex,mousey) and click :
            menuOffset -= 1
    if menuOffset < len(g) - 1 :
        menu_right = pygame.Rect((550, 160), (50, 100))
        pygame.draw.polygon(window, BLUE, ((550, 160), (550, 260), (600, 210)))
        if menu_right.collidepoint(mousex, mousey) and click :
            menuOffset += 1

    menu = robC.render("Menu", True, YELLOW, PURPLE) # return to menu button
    mect = menu.get_rect()
    mect.center = (70, 25)
    window.blit(menu, mect)
    if mect.collidepoint(mousex, mousey) and click :
        frame = 1


########################################################################################################################
####################################################      Player     ###################################################
def player_died() : # this function is a sequence that will be triggered every time player smashes into something (fails)
    global hiScore, level_offset, gravity, jumpForce, inJump, onGround, initJump, walls, jump_pads, spikes
    if hiScore < level_offset : # check hi-score
            hiScore = level_offset # apply new value

    # reset variables
    gravity = 0
    jumpForce = 0
    inJump = False
    onGround = False
    pygame.mixer.music.rewind()

    for z in range(0, len(walls)) :
        walls[z].centerx -= level_offset

    for z in range(0, len(spikes)) :
        spikes[z].centerx -= level_offset

    for z in range(0, len(jump_pads)) :
        jump_pads[z].centerx -= level_offset

    level_offset = 0


def jump(force) :
    global inJump, jumpForce, initJump, onGround
    if not inJump :
        initJump = force
        jumpForce = force
        inJump = True
        onGround = False


def player_movement() :
    global level_offset, gravity, onGround, hiScore, jumpForce, inJump, initJump, player_pos_y, walls, spikes, jump_pads, player_rotation, old_angle, angle, playerSurface, angle_state, oldJump
    player_y = 240

    player_pos_y = player_y + gravity - jumpForce

    player_position = pygame.Rect((120, player_pos_y), (60, 60)) # set up position of player

    if click and onGround : #jump action
        jump(15)

    for this_pad in jump_pads :
        if player_position.collidepoint(this_pad.center) : # jump pad detection, can NOT activate in air
            jump(21)

    if inJump : # jump is separated from gravity as gravity will override proper sequence of acceleration
        jumpForce = jumpForce + initJump - 1
        initJump -= 1

    if not onGround and not inJump:
        gravity += 10

    player_pos_y = player_y + gravity - jumpForce
    player_position.y = player_pos_y

    onGround = False
    for wall in walls :
        if 90 < wall.centerx < 210 and wall.top < player_position.bottom + 59 : # if player is not on ground
            if -10 < wall.top - player_position.bottom < 10 : #
                player_pos_y = wall.top - 60
                gravity += player_pos_y - (player_y + gravity)
                jumpForce = 0
                initJump = 0
                onGround = True
                inJump = False

    smashed = player_position.collidelist(walls)
    spiked = player_position.collidelist(spikes) # determines if player has smashed into any of the spikes that are available in the level to reset
    if spiked >= 0 or player_pos_y > 900 or smashed >= 0:
        player_died()

    if click and onGround : #jump action
        jump(15)

    travel = math.sqrt((oldJump - jumpForce) ** 2 + 144)
    angle = math.degrees(math.acos(12 / travel))# get movement angle
    oldJump = jumpForce
    bsa = angle
    if angle > old_angle != 0:
        angle = 0 - angle

    old_angle = bsa
    if old_angle == 1 :
        angle -= 180

    new_surface = pygame.transform.rotate(playerSurface, angle)
    window.blit(new_surface, player_position)


########################################################################################################################
#####################################################      Level     ###################################################
def reset_level_data() :
    global walls, spikes, jump_pads
    for i in range(0, len(walls)) :
        a = walls.pop(0)
    for i in range(0, len(spikes)) :
        a = spikes.pop(0)
    for i in range(0, len(jump_pads)) :
        a = jump_pads.pop(0)


def load_level():
    global menuOffset, level_offset, frame, player_pos_y, walls, jump_pads, spikes, levelSurface
    walls = []
    jump_pads = []
    spikes = []
    reset_level_data()
    selected_level = g[menuOffset]

    width = int(len(selected_level[0]) * 60)
    levelSurface = pygame.Surface((width, 480), SRCALPHA)
    for a in range(0, len(selected_level[0]) - 1) : # levels must be with 1 extra column as to prevent from random a peculiar bug of "new line syndrome"
                                                    # this but is in the mean of last row of last level holds no "new line" or \n in it
                                                    # and since len() method counts \n as a char, last line becomes shorter than first line in the last level
                                                    # other solution may be of adding an extra character in the end of last line or adding next line
                                                    # but these solutions are "hard-coded", thus useless
        for i in range(0, len(selected_level)) :
            # asset index: w h <^v> s j p .
            # wallNormal/wallHazard/spikeLeft/spikeUp/spikeRight/spikeDown/smallSpike/jumpPad/plato/empty
            # these if statements serve as a level generator by utilizing a 60x60 px grid
            h = pygame.Rect((60 * a, 60 * i), (60, 60)) # reduce the number of elements on screen
            if selected_level[i][a] == 'h' :
                levelSurface.blit(WallHz, h)
                walls.append(h)
            elif selected_level[i][a] == 'w' :
                levelSurface.blit(WallBr, h)
                walls.append(h)
            elif selected_level[i][a] == '<' :
                sl = pygame.Rect((60 * a + 10, 60 * i + 20), (50, 20))
                levelSurface.blit(SpikeLf, h)
                spikes.append(sl)
            elif selected_level[i][a] == '^' :
                su = pygame.Rect((60 * a + 20, 60 * i + 10), (20, 50))
                levelSurface.blit(SpikeUp, h)
                spikes.append(su)
            elif selected_level[i][a] == '>' :
                sr = pygame.Rect((60 * a + 10, 60 * i), (50, 20))
                levelSurface.blit(SpikeRt, h)
                spikes.append(sr)
            elif selected_level[i][a] == 'v' :
                sd = pygame.Rect((60 * a + 20, 60 * i), (20, 50))
                levelSurface.blit(SpikeDw, h)
                spikes.append(sd)
            elif selected_level[i][a] == 's' :
                s = pygame.Rect((60 * a, 60 * i + 45), (60, 15))
                levelSurface.blit(SpikeSm, s)
                spikes.append(s)
            elif selected_level[i][a] == 'p' :
                p = pygame.Rect((60 * a, 60 * i), (60, 15))
                levelSurface.blit(plato, p)
                walls.append(p)
            elif selected_level[i][a] == 'j' :
                j = pygame.Rect((60 * a, 60 * i), (60, 15))
                levelSurface.blit(pad, j)
                jump_pads.append(j)


def run_level() : # uses global variables that were set in level selection to run desired level instead of them being passed by, this is because of implementing "frame" UI design
    global hiScore, walls, spikes, jump_pads, frame, loaded, level_offset, levelSurface, g
    level_offset -= 12
    if not loaded :
        load_level()
        loaded = True

    player_movement()

    for z in range(0, len(walls)) :
        walls[z].centerx -= 12

    for z in range(0, len(spikes)) :
        spikes[z].centerx -= 12

    for z in range(0, len(jump_pads)) :
        jump_pads[z].centerx -= 12
    window.blit(levelSurface, ((level_offset, 0), (480, len(g[menuOffset][0]) * 60)))

    exit_button = robC.render("Exit", True, YELLOW, PURPLE)
    exit_rect = exit_button.get_rect()
    exit_rect.center = (70, 25)
    window.blit(exit_button, exit_rect)

    if (exit_rect.collidepoint(mousex, mousey) and click) or (-1 * level_offset > (len(g[menuOffset][0]) - 2) * 60) : # goto score or end of level
        if hiScore < -1 * level_offset:
            hiScore = -1 * level_offset
        loaded = False
        player_died()
        frame = 4
        pygame.mixer.music.load('assets/menu.mp3')
        pygame.mixer.music.play()


########################################################################################################################
#####################################################      Score     ###################################################
def game_score() :
    global frame, hiScore, menuOffset, BG, called, board
    if not called :
        Scores.send_score(user, levelHead[menuOffset][0], hiScore) # calls and checks on current hiscore
        board = Scores.get_scores(levelHead[menuOffset][0])
        called = True

    for i in range(0, len(board)) : # striped scoreboard for levels
        position = i * 40 + 30
        base_rect = pygame.Rect(200, position, 400, 40) # shows score
        BG = None
        if i % 2 == 0 :
            BG = PURPLE
        else :
            BG = BLUE

        pygame.draw.rect(window, BG, base_rect)
        nickname = robN.render(str(board[i][0]), True, YELLOW, BG)
        window.blit(nickname, base_rect)

        nick_score = robN.render(str(board[i][1]), True, YELLOW, BG) # render the board at location that was specified
        base_rect_2 = nick_score.get_rect()
        base_rect_2.centery = base_rect.centery
        base_rect_2.left = 450
        window.blit(nick_score, base_rect_2)

    exit_button = robN.render("Continue", True, YELLOW, PURPLE)
    exit_rect = exit_button.get_rect()
    exit_rect.center = (400, 455)
    window.blit(exit_button, exit_rect)
    if exit_rect.collidepoint(mousex, mousey) and click :
        frame = 1
        hiScore = 0


########################################################################################################################
##################################################      Game Loop     ##################################################
while True : # game loop
    click = False
    if not last_click :
        click = pygame.mouse.get_pressed()[0]

    mousex, mousey = pygame.mouse.get_pos()

    if click :
        last_click = True
        bgCol = (random.randint(60, 255), random.randint(60, 255), random.randint(60, 255)) # get new bgcolor for every click

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
            Scores.finish()
            pygame.quit()
            sys.exit()
        if event.type == MOUSEBUTTONUP :
            last_click = False

    pygame.display.update()
    frameRate.tick(60)

########################################################################################################################
#################################################  END  ################################################################
########################################################################################################################