# Handle Gobblets and their locations on board
import pygame
import sys
import os
import math
from Game import Game
from Postion import Postion

#GUI
from GameView import *
from EventHandling import *
import Global_variables

def Black_Gobblets_Init_Positions():

    Black_Gobblets_rect=GV.Black_Gobblets_rect
    Black_Gobblets_rect = [[None for _ in range(4)] for _ in range(4)]

    for x in range (4):
        for y in range (3):
            Black_Gobblets_rect[x][y] = Black_Gobblets[x][y].get_rect() 
            Black_Gobblets_rect[x][y].x = 80 + (x * 10)
            Black_Gobblets_rect[x][y].y = 100 + (x * 10) + (y * 100)



def Draw_Black_Gobblets():
    GV.Black_Gobblets = [[None for _ in range(4)] for _ in range(4)]

    for x in range (4):
        for y in range (3):
            GV.Black_Gobblets[x][y] = pygame.image.load(".\\Images\\black_gobblet.png")  
 

    for i in range (4):
        GV.Black_Gobblets[i][0] = pygame.transform.scale(Black_Gobblets[i][0], (100 - 20 * i, 100 - 20 * i))
        GV.Black_Gobblets[i][1] = pygame.transform.scale(Black_Gobblets[i][1], (100 - 20 * i, 100 - 20 * i))
        GV.Black_Gobblets[i][2] = pygame.transform.scale(Black_Gobblets[i][2], (100 - 20 * i, 100 - 20 * i))


    Black_Gobblets_Init_Positions()

    Display_Black_Gobblets()



    

  

def Display_Black_Gobblets():
    
    for x in range (4):
        for y in range (3):
            # Display the images on the screen
            screen.blit(GV.Black_Gobblets[3 - x][2 - y], GV.Black_Gobblets_rect[3 - x][2 - y])

    pygame.display.flip()





def White_Gobblets_Init_Positions():
    
    

    GV.White_Gobblets_rect = [[None for _ in range(4)] for _ in range(4)]

    for x in range (4):
        for y in range (3):
            Gv.White_Gobblets_rect[x][y] = GV.White_Gobblets[x][y].get_rect() 
            GV.White_Gobblets_rect[x][y].x = 630 + (x * 10)
            GV.White_Gobblets_rect[x][y].y = 100 + (x * 10) + (y * 100)






def Draw_White_Gobblets():
    
    
    GV.White_Gobblets = [[None for _ in range(4)] for _ in range(4)]

    for x in range (4):
        for y in range (3):
            GV.White_Gobblets[x][y] = pygame.image.load(".\\Images\\white_gobblet.png")  
 

    for i in range (4):
        GV.White_Gobblets[i][0] = pygame.transform.scale(White_Gobblets[i][0], (115 - 20 * i, 115 - 20 * i))
        GV.White_Gobblets[i][1] = pygame.transform.scale(White_Gobblets[i][1], (115 - 20 * i, 115 - 20 * i))
        GV.White_Gobblets[i][2] = pygame.transform.scale(White_Gobblets[i][2], (115 - 20 * i, 115 - 20 * i))


    White_Gobblets_Init_Positions()

    Display_White_Gobblets()
    

    pygame.display.flip()


def Display_White_Gobblets():
   
    for x in range (4):
        for y in range (3):
            # Display the images on the screen
            screen.blit(GV.White_Gobblets[3 - x][2 - y], GV.White_Gobblets_rect[3 - x][2 - y])

    pygame.display.flip()




