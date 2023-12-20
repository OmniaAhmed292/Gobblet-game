import pygame
import sys
import os
import math
from Game import Game
from Postion import Postion

#GUI
from GameView import *
from Draw_Gobblets import *
from EventHandling import *
import Global_variables



# # Imports For Logiv

# from AIPlayer import AIPlayer
# from HumanPlayer import HumanPlayer





def main():
    game1 = Game("Hanan", "omnia")
    game1.print_grid()
    
    #pile  # 4, 4, 4
    game1.do_turn(0, Postion(1, 1), from_pile=3) #pile : 4, 4, 3
    game1.print_grid()
    game1.do_turn(0, Postion(1, 2), from_pile=1) #pile: 3, 4,3
    game1.print_grid()
    game1.do_turn(0, Postion(1, 3), from_pile=3) #pile: 3,4,2
    game1.print_grid()
    game1.do_turn(0, Postion(1, 0), from_pile=2) #pile: 3,3,2 
    game1.print_grid()
    '''
    game1.do_turn(0, Postion(1, 2), from_grid=Postion(1, 1))
    game1.print_grid()
    game1.do_turn(0, Postion(1, 0), from_pile=2)
    game1.print_grid() '''




# Main function to run the game
if __name__ == "__main__":
    initialize_pygame()
    load_images()
    initialize_fonts()
    initialize_buttons()
    Events_Handler()

    pygame.quit()
    sys.exit()
