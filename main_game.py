#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Nov 28 12:47:54 2017

@author: kalenga
"""

import pygame
from pygame.locals import *
from random import randint
from case import Case
from input_text import Input
import string
from math import sin
import time
import sys
sys.setrecursionlimit(1500)


def build_grid(nb_rows, nb_cols):
    grid=[]
    for i in range(nb_rows):
        line=[]
        for j in range(nb_cols):
            line.append(Case(i,j))
        grid.append(line)
    return grid

def neighbors(i,j,grid):
    voisins=[]
    height=len(grid)
    width=len(grid[0])
    if i>0:
        voisins.append(grid[i-1][j])
        if j>0:
            voisins.append(grid[i-1][j-1])
        if j<width-1:
            voisins.append(grid[i-1][j+1])
    if i<height-1:
        voisins.append(grid[i+1][j])
        if j>0:
            voisins.append(grid[i+1][j-1])
        if j<width-1:
            voisins.append(grid[i+1][j+1])
    if j>0:
        voisins.append(grid[i][j-1])
    if j<width-1:
        voisins.append(grid[i][j+1])
    return voisins
            
def expose_vacuity(i,j,grid):
    grid[i][j].up_n_reveal()
    voisins=neighbors(i,j,grid)
    if grid[i][j].value=="Empty":
        for voisin in voisins:
            if voisin.status!="revealed":
                expose_vacuity(voisin.i, voisin.j, grid)
            
def whats_my_score(grid,score_to_reach):
    score=0
    for line in grid:
        for case in line:
            if case.status=="revealed" and case.value!="RevealedMine" and case.value!="ExplodedMine":
                score+=1
    if score==score_to_reach:
        score = 100*(score/score_to_reach)
        score = int(100*score)/100
        print("score", score, "%")
        return True, score
    else:
        score = 100*(score/score_to_reach)
        score = int(100*score)/100
        print("score", score, "%")
        return False, score
    
def is_inside(i,j,grid):
    height=len(grid)
    width=len(grid[0])
    width_pixel = 24*width
    height_pixel=24*height
    if i>=height_pixel or j>=width_pixel:
        return False
    else:
        return True
    
def is_inside_box(pos,box):
    if box.bottom>pos[1]>box.top and box.left<pos[0]<box.right:
        return True
    else:
        return False
    
def grid_to_background(screen, grid):
    background = pygame.Surface((screen.get_width(),screen.get_height()))
    for line in grid:
        for case in line:
            background.blit(case.cell,(case.j_pixel,case.i_pixel))
    return background

def play_sound_case(case):
    pygame.mixer.stop()
    case.sound.play()
    
def play_sound(sound):
    pygame.mixer.stop()
    son = pygame.mixer.Sound("./sounds/"+sound+".wav")
    son.set_volume(0.25)
    son.play()
    
def start_intro():
    #Building the window frame
    screen = pygame.display.set_mode((320,240))
    pygame.font.init()
    strings = ["", "", ""]
    width_box = Input(screen,1,"Width")
    height_box = Input(screen,2,"Height")
    mines_box = Input(screen,3,"How many mines")
    boxes=[width_box,height_box,mines_box]
    for box in boxes:
        box.display("")
    pygame.display.flip()
    current_box = boxes[0]
    current_string = strings[0]
    current_box.focus_yourself()
    continuer = 1
    while continuer:
        for event in pygame.event.get():
            
            if event.type == QUIT:
                pygame.quit()
        
            if event.type == MOUSEBUTTONDOWN and event.button == 1:
                for box in boxes:
                    if is_inside_box(event.pos,box):
                        current_box.unfocus_yourself()
                        current_box=box
                        current_box.focus_yourself()
                        current_string=strings[current_box.position-1]
            
            if event.type == KEYDOWN:
                inkey=event.key
                if inkey == K_BACKSPACE:
                    current_string = current_string[0:-1]
                elif inkey == K_RETURN:
                    continuer = 0
                elif inkey == K_MINUS:
                    current_string+="_"
                elif inkey == K_TAB:
                    current_box.unfocus_yourself()
                    current_box=boxes[current_box.position%3]
                    current_box.focus_yourself()
                    current_string=strings[current_box.position-1]
                elif inkey == K_UP or inkey == K_LEFT:
                    current_box.unfocus_yourself()
                    current_box=boxes[(current_box.position-2)%3]
                    current_box.focus_yourself()
                    current_string=strings[current_box.position-1]
                elif inkey == K_DOWN or inkey == K_RIGHT:
                    current_box.unfocus_yourself()
                    current_box=boxes[current_box.position%3]
                    current_box.focus_yourself()
                    current_string=strings[current_box.position-1]
                else:
                    if len(current_string)<current_box.symbol_limit:
                        current_string+=event.unicode
                current_box.display(current_string)
                strings[current_box.position-1] = current_string
                pygame.display.flip()
                
    int_count=0
    for string in strings:
        if sum([47<ord(i)<58 for i in string])==len(string) and len(string)>0:
            int_count+=1
    if int_count==3:
        play_sound("ok")
        return int(strings[0]), int(strings[1]), int(strings[2])
    else:
        print("These are not three integers")
        print("The default parameters will then be:")
        print("Width: 30     Height: 16     Number of mines: 80")
        play_sound("ok")
        return 30,16,80
            
def initialize_grid(width, height,nb):
    #Building the window frame
    width_pixel = 24*width
    height_pixel=24*height
    window = pygame.display.set_mode((width_pixel, height_pixel))
    mines=[]
    score_to_reach = width*height-nb
    
    #Building the grid object and placing the mines
    grid=[]
    if nb == 0:
        for i in range(height):
            line=[]
            for j in range(width):
                line.append(Case(i,j,window, "Empty"))
            grid.append(line)
    elif nb>width*height:
        for i in range(height):
            line=[]
            for j in range(width):
                line.append(Case(i,j,window, "RevealedMine"))
            grid.append(line)
    else:
        if width*height>2*nb:
            for i in range(height):
                line=[]
                for j in range(width):
                    line.append(Case(i,j,window, "Empty"))
                grid.append(line)
            mines_posed=0
            while mines_posed<nb:
                i = randint(0,height-1)
                j = randint(0,width-1)
                if grid[i][j].value == "Empty":
                    grid[i][j].set_value("RevealedMine")
                    mines.append({"i":i,"j":j})
                    mines_posed+=1
        else:
            for i in range(height):
                line=[]
                for j in range(width):
                    line.append(Case(i,j,window, "RevealedMine"))
                grid.append(line)
                empty_posed=0
            while empty_posed<width*height-nb:
                i = randint(0,height-1)
                j = randint(0,width-1)
                if grid[i][j].value == "RevealedMine":
                    grid[i][j].set_value("Empty")
                    empty_posed+=1
                    
                    
    #Setting the cases values when next to a mine
    for line in grid:
        for case in line:
            if case.value=="RevealedMine":
                voisins=neighbors(case.i,case.j,grid)
                for voisin in voisins:
                    voisin.increment_value()
    
    #Setting the sounds
    for line in grid:
        for case in line:
            case.set_sound()
                    
    #Drawing the grid on the window
    for line in grid:
        for case in line:
            #Careful here (i,j) is matrix coordinate whereas (width,height) is pixel coordinates, not same axis
            window.blit(case.cell,(case.j_pixel,case.i_pixel))

    pygame.display.flip()
    return grid,window, mines, score_to_reach
    
def start_game(grid,window, mines, score_to_reach):

    #Some variables
    is_mouse_button_down=False
    current_case=grid[0][0]
    previous_case=grid[0][0]
    continuer = 1
    final_result="lose"
    score = 0
    
######################## Main loop ############################################

   
    #Game loop
    game_continue=1
    while game_continue:
        pygame.time.Clock().tick(30)
        
        for event in pygame.event.get():
            
            if event.type == QUIT:
                pygame.quit()
            
            if event.type == KEYDOWN:
                if event.key == K_q:
                    continuer = 0
                    game_continue=0
                else:
                    print("keydown")
                    
            if event.type == MOUSEBUTTONDOWN and (event.button == 1 or event.button == 3):
                if is_inside(event.pos[1],event.pos[0],grid):
                    is_mouse_button_down=True
                    current_case.down()
                
            if event.type == MOUSEBUTTONUP and event.button == 1:
                if is_inside(event.pos[1],event.pos[0],grid):
                    is_mouse_button_down=False
                    if current_case.value == "RevealedMine":
                        current_case.set_value("ExplodedMine")
                        current_case.up_n_reveal()
                        for mine in mines:
                            grid[mine['i']][mine['j']].up_n_reveal()
                        final_result="lose"
                        play_sound_case(current_case)
                        game_continue=0
                    elif current_case.value == "Empty":
                        expose_vacuity(current_case.i,current_case.j,grid)
                        pygame.display.flip()
                        play_sound_case(current_case)
                    else:
                        current_case.up_n_reveal()
                        play_sound_case(current_case)
                    did_I_just_win, score = whats_my_score(grid,score_to_reach)
                    if did_I_just_win:
                        for mine in mines:
                            grid[mine['i']][mine['j']].up_n_reveal()
                        final_result="win"
                        play_sound("just_win")
                        game_continue=0
                    
            if event.type == MOUSEBUTTONUP and event.button == 3:
                if is_inside(event.pos[1],event.pos[0],grid):
                    is_mouse_button_down=False
                    current_case.toogle_flag()
                    pygame.mixer.Sound("./sounds/unflag.wav").play()
                
            if event.type == MOUSEMOTION and is_mouse_button_down:
                if is_inside(event.pos[1],event.pos[0],grid):
                    i = event.pos[1]//24
                    j = event.pos[0]//24
                    if grid[i][j] != current_case:
                        previous_case=current_case
                        current_case=grid[i][j]
                        current_case.down()
                        previous_case.up()
                    
            if event.type == MOUSEMOTION:
                if is_inside(event.pos[1],event.pos[0],grid):
                    i = event.pos[1]//24
                    j = event.pos[0]//24
                    if grid[i][j] != current_case:
                        previous_case=current_case
                        current_case=grid[i][j]

###################### End of the Game loop ###################################                    
    print(final_result)
    return score, final_result


def fade_in_out(screen, grid, position, text, text_size, final_result):
    #Getting the background
    background = grid_to_background(screen, grid)
    #Getting the image or text
#    img = pygame.image.load("./assets/"+image_name).convert()
    font = pygame.font.SysFont('sans-serif', text_size, True)
    img = font.render(text, True, (255, 255, 255),(0,0,0)).convert()
    img_rect = img.get_rect(center=position)
    #Initializing the timer
    start = time.time()
    #Starting the loop
    is_admiring_result = 1
    while is_admiring_result:
        screen.blit(background, (0,0))
        
        for event in pygame.event.get():
            
            if event.type == QUIT:
                pygame.quit()
                
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == KEYDOWN:
                if event.key == K_RETURN:
                    is_admiring_result = 0
        
        t= time.time() - start
        img.set_alpha(int(sin(t)*255))
        screen.blit(img, img_rect)
        pygame.display.flip()
    play_sound(final_result)
############# End of the Fade loop ############################################
    

def wanna_play_again(score, final_result):
    #Building the window frame
    screen = pygame.display.set_mode((320,340))
    pygame.font.init()
    score_box = Input(screen,1,"Score")
    score_box.display(str(score)+"%")
    result = pygame.image.load("./assets/"+final_result+".png").convert_alpha()
    screen.blit(result, ((screen.get_width()-result.get_width())/2, (screen.get_height()-result.get_height())/2))
    text_box = Input(screen,3,"Do you want to play again")
    text_box.display("")
    yes = pygame.image.load('./assets/yes.png').convert_alpha()
    yes_pressed = pygame.image.load('./assets/yesPressed.png').convert_alpha()
    no = pygame.image.load('./assets/no.png').convert_alpha()
    no_pressed = pygame.image.load('./assets/noPressed.png').convert_alpha()
    yes_position=(50,280)
    no_position=(170,280)
    yes_limits={'top':yes_position[1], 'bottom':yes_position[1]+45, 'left':yes_position[0], 'right':yes_position[0]+100}
    no_limits={'top':no_position[1], 'bottom':no_position[1]+45, 'left':no_position[0], 'right':no_position[0]+100}
    screen.blit(yes,yes_position)
    screen.blit(no,no_position)
    pygame.display.flip()
    
    is_choosing = 1
    want_to_continue = "Hope"
    is_button_pressed = False
    is_choosing_with_keyboard = False
    while is_choosing:
        for event in pygame.event.get():
            
            if event.type == QUIT:
                pygame.quit()
                
            if event.type == MOUSEBUTTONDOWN and event.button == 1:
                if yes_limits['left']<event.pos[0]<yes_limits['right'] and yes_limits['top']<event.pos[1]<yes_limits['bottom']:
                    screen.blit(yes_pressed,yes_position)
                    screen.blit(no,no_position)
                    pygame.display.flip()
                    is_button_pressed = True
                elif no_limits['left']<event.pos[0]<no_limits['right'] and no_limits['top']<event.pos[1]<no_limits['bottom']:
                    screen.blit(no_pressed,no_position)
                    screen.blit(yes,yes_position)
                    pygame.display.flip()
                    is_button_pressed = True
                    
            if event.type == MOUSEBUTTONUP and event.button == 1:
                if is_button_pressed:
                    screen.blit(yes,yes_position)
                    screen.blit(no,no_position)
                    pygame.display.flip()
                    is_button_pressed = False
                    if yes_limits['left']<event.pos[0]<yes_limits['right'] and yes_limits['top']<event.pos[1]<yes_limits['bottom']:
                        want_to_continue = True
                        is_choosing = False
                    elif no_limits['left']<event.pos[0]<no_limits['right'] and no_limits['top']<event.pos[1]<no_limits['bottom']:
                        want_to_continue = False
                        is_choosing = False

            if event.type == KEYDOWN:
                    if event.key == K_q:
                        want_to_continue = False
                        is_choosing = 0
                    if event.key == K_LEFT:
                        is_choosing_with_keyboard = True
                        want_to_continue = True
                        screen.blit(yes_pressed,yes_position)
                        screen.blit(no,no_position)
                        pygame.display.flip()
                    if event.key == K_RIGHT:
                        is_choosing_with_keyboard = True
                        want_to_continue = False
                        screen.blit(no_pressed,no_position)
                        screen.blit(yes,yes_position)
                        pygame.display.flip()
                    if event.key == K_RETURN:
                        if is_choosing_with_keyboard:
                            is_choosing = False
                    if event.key == K_UP or event.key == K_DOWN:
                        is_choosing_with_keyboard = False
                        screen.blit(yes,yes_position)
                        screen.blit(no,no_position)
                        pygame.display.flip()
                            
###################### End of the choosing loop ##############################
    pygame.mixer.stop()
    return want_to_continue
                        
def just_play_the_game():
    pygame.init()
    width, height, mine_number = start_intro()
    grid, window, mines, score_to_reach = initialize_grid(width,height,mine_number)
    continuer = 1
    while continuer:
        score, final_result = start_game(grid, window, mines, score_to_reach)
        fade_in_out(window,grid,(window.get_width()/2,window.get_height()/5),"PRESS ENTER", int(window.get_height()/6), final_result)
        want_to_continue = wanna_play_again(score, final_result)
        if want_to_continue:
            grid, window, mines, score_to_reach = initialize_grid(width,height,mine_number)
            continue
        else:
            continuer = 0
    pygame.quit()
    print("it's over")
                

