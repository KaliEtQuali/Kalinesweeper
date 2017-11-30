#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Nov 28 13:17:09 2017

@author: kalenga
"""

import pygame

class Case:
    def __init__(self, i, j, window,value):
        self.i = i
        self.j = j
        self.i_pixel = i*24
        self.j_pixel = j*24
        self.value = value
        self.cell = pygame.image.load("./assets/Cell.png").convert()
        self.cell_down = pygame.image.load("./assets/CellDown.png").convert()
        self.previous_cell = pygame.image.load("./assets/"+str(value)+"Cell.png")
        self.window = window
        self.flag_status = "not flagged"
        self.status = "nada so far"
        self.sound = "whatever"
        
    def __repr__(self):
        return "Case {},{}".format(self.i, self.j) 
    
    def down(self):
        self.window.blit(self.cell_down, (self.j_pixel, self.i_pixel))
        pygame.display.flip()

    def up(self):
        self.window.blit(self.cell, (self.j_pixel, self.i_pixel))
        pygame.display.flip()
        
    def up_n_reveal(self):
        self.cell = pygame.image.load("./assets/"+str(self.value)+"Cell.png")
        self.status = "revealed"
        self.window.blit(self.cell, (self.j_pixel, self.i_pixel))
        pygame.display.flip()
        
    def set_value(self,value):
        self.value=value
        
    def toogle_flag(self):
        if self.status != "revealed":
            if self.flag_status == "not flagged":
                self.previous_cell = self.cell
                self.cell = pygame.image.load("./assets/FlaggedCell.png")
                self.window.blit(self.cell, (self.j_pixel, self.i_pixel))
                self.flag_status = "flagged"
                pygame.display.flip()
            elif self.flag_status == "flagged":
                self.cell = self.previous_cell
                self.window.blit(self.cell, (self.j_pixel, self.i_pixel))
                self.flag_status = "not flagged"
                pygame.display.flip()
        else:
            self.up()
    
    def increment_value(self):
        if self.value!="RevealedMine":
            if self.value=="Empty":
                self.value=1
            else:
                self.value+=1
    def set_sound(self):
        if type(self.value) == int:
            self.sound = pygame.mixer.Sound("./sounds/1.wav")
            self.sound.set_volume(0.25)
        else:
            self.sound = pygame.mixer.Sound("./sounds/"+self.value+".wav")
            self.sound.set_volume(0.25)
    
    
            
    