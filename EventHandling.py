    #Handle Events and Display of their actions
import pygame
import sys
import os
import math
from Game import Game
from Postion import Postion
#GUI
from GameView import *
from Draw_Gobblets import *
import Global_variables as GV

def move_gobblet(Gobblet_rect, grid_centers_tuple):
    
    draw_game_board()

    for x in range (4):
        for y in range (3):

            if(Gobblet_rect == Black_Gobblets_rect[x][y]):
                Black_Gobblets_rect[x][y].x = grid_centers_tuple[0]
                Black_Gobblets_rect[x][y].y = grid_centers_tuple[1]

                Display_Black_Gobblets()
                Display_White_Gobblets()

            elif(Gobblet_rect == White_Gobblets_rect[x][y]):
                White_Gobblets_rect[x][y].x = grid_centers_tuple[0]
                White_Gobblets_rect[x][y].y = grid_centers_tuple[1]

                Display_Black_Gobblets()
                Display_White_Gobblets()


    pygame.display.flip()


def Move_Human_Goblet():

    clicked = False

    # First click: select the image
    mouse_pos = pygame.mouse.get_pos()
    
    for x in range (4):
        for y in range (3):

            if(mode_selection == "human_vs_human"):

                if(turn == "P1"):
                    if (Black_Gobblets_rect[3- x][2 - y].collidepoint(mouse_pos)):
                        selected_image = Black_Gobblets_rect[3 - x][2 - y]
                        clicked = True

                elif(turn == "P2"):
                    if (White_Gobblets_rect[3 - x][2 - y].collidepoint(mouse_pos)):
                        selected_image = White_Gobblets_rect[3 - x][2- y]
                        clicked = True

            elif(mode_selection == "hard_ai_vs_human"):
                
                if(turn == "P1"):
                    if (Black_Gobblets_rect[3- x][2 - y].collidepoint(mouse_pos)):
                        selected_image = Black_Gobblets_rect[3 - x][2 - y]
                        clicked = True

                elif(turn == "P2"):
                    return

            elif(mode_selection == "easy_ai_vs_human"):
                
                if(turn == "P1"):
                    if (Black_Gobblets_rect[3- x][2 - y].collidepoint(mouse_pos)):
                        selected_image = Black_Gobblets_rect[3 - x][2 - y]
                        clicked = True

                elif(turn == "P2"):
                    return

    while clicked == True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            elif event.type == pygame.MOUSEBUTTONDOWN and clicked:
                # Second click: move the image
                mouse_pos = pygame.mouse.get_pos()
                #minimum = math.sqrt(Table_centers[0][0][0] ** 2 + Table_centers[0][0][1] ** 2)
                i = 0
                j = 0

                for x in range (4):

                    if(mouse_pos[0] > (200 + x * 100) and mouse_pos[0] < (200 + (x + 1) * 100)):
                        i = x

                    if(mouse_pos[1] > (100 + x * 100) and mouse_pos[1] < (100 + (x + 1) * 100)):
                        j = x



                if selected_image:
                    move_gobblet(selected_image, Table_centers[i][j])
                    clicked = False
                    selected_image = None

    if(turn == "P1"):
        turn = "P2"

    elif(turn == "P2"):
        turn = "P1"
             


# Main Game Loop
def Events_Handler():


    mode_selection = "start_menu"  # Default mode
    previous_mode = ""  # Track previous mode

    Game_Handler(mode_selection)

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                print("Mouse pressed")
                if back_button_rect.collidepoint(event.pos):
                    # Go back to the previous mode when back button is clicked
                    mode_selection = previous_mode
                    Game_Handler(mode_selection)
                elif mode_selection == "start_menu":
                    if human_vs_human_button.collidepoint(event.pos):
                        # Handle Human vs Human mode selection
                        previous_mode = mode_selection  # Assign previous mode before changing
                        mode_selection = "Enter_Names"  # Transition to Human vs Human mode
                        Game_Handler(mode_selection)
                    elif human_vs_computer_button.collidepoint(event.pos):
                        previous_mode = mode_selection
                        mode_selection = "ai_vs_human_difficulty_selection"  # Transition to Human vs Computer Difficulty selection mode
                        print("Entered Human V Computer Difficulty Selection mode")
                        Game_Handler(mode_selection)
                    elif computer_vs_computer_button.collidepoint(event.pos):
                        previous_mode = mode_selection
                        mode_selection = "ai_1_difficulty_selection"  # Transition to Computer vs Computer Difficulty selection mode
                        print("Entered Computer V Computer Difficulty Selection mode")
                        Game_Handler(mode_selection)
                elif mode_selection == "Enter_Names":
                    # Handle input fields for player names
                    if player1_input_rect.collidepoint(event.pos):
                        active_input = player1_input_rect
                    elif player2_input_rect.collidepoint(event.pos):
                        active_input = player2_input_rect

                    elif Enter_Button_rect.collidepoint(event.pos):
                        previous_mode = mode_selection
                        mode_selection = "human_vs_human"  
                        Game_Handler(mode_selection)
                    else:
                        active_input = None
                        
                elif mode_selection == "ai_vs_human_difficulty_selection":
                    
                    if hard_button.collidepoint(event.pos):
                        # Handle ai_vs_human_difficulty_selection mode selection
                        previous_mode = mode_selection  # Assign previous mode before changing
                        mode_selection = "hard_ai_vs_human" 
                        Game_Handler(mode_selection)
                        
                    elif easy_button.collidepoint(event.pos):
                        # Handle ai vs Human mode selection
                        previous_mode = mode_selection  # Assign previous mode before changing
                        mode_selection = "easy_ai_vs_human" 
                        Game_Handler(mode_selection)
                elif mode_selection == "ai_1_difficulty_selection":
                    
                    if hard_button.collidepoint(event.pos):
                        ai_1_difficulty = "hard"
                        # Handle ai_vs_ai_difficulty_selection mode selection
                        previous_mode = mode_selection  # Assign previous mode before changing
                        mode_selection = "ai_2_difficulty_selection" 
                        Game_Handler(mode_selection)
                        
                    elif easy_button.collidepoint(event.pos):
                        ai_1_difficulty = "easy"
                        # Handle ai vs ai mode selection
                        previous_mode = mode_selection  # Assign previous mode before changing
                        mode_selection = "ai_2_difficulty_selection" 
                        Game_Handler(mode_selection) 
                elif mode_selection == "ai_2_difficulty_selection":
                    
                    if hard_button.collidepoint(event.pos):
                        ai_2_difficulty = "hard"
                        # Handle ai_vs_ai_difficulty_selection mode selection
                        previous_mode = mode_selection  # Assign previous mode before changing
                        mode_selection = "Computer_vs_Computer" 
                        Game_Handler(mode_selection)
                        
                    elif easy_button.collidepoint(event.pos):
                        ai_2_difficulty = "easy"
                        # Handle ai vs ai mode selection
                        previous_mode = mode_selection  # Assign previous mode before changing
                        mode_selection = "Computer_vs_Computer" 
                        Game_Handler(mode_selection)
                        
                elif mode_selection == "easy_ai_vs_human" or mode_selection == "hard_ai_vs_human" or mode_selection == "human_vs_human":
                     Move_Human_Goblet()

            elif event.type == pygame.KEYDOWN:
                if mode_selection == "Enter_Names" and active_input:
                    # Handle keyboard input for entering player names
                    if event.key == pygame.K_RETURN:
                        active_input = None
                    elif event.key == pygame.K_BACKSPACE:
                        if active_input == player1_input_rect:
                            player1_name = player1_name[:-1]
                        elif active_input == player2_input_rect:
                            player2_name = player2_name[:-1]
                    else:
                        if active_input == player1_input_rect and len(player1_name) < 15:
                            player1_name += event.unicode
                        elif active_input == player2_input_rect and len(player2_name) < 15:
                            player2_name += event.unicode

                
                # Draw input fields for player names
                pygame.draw.rect(screen, (255, 255, 255), player1_input_rect)
                pygame.draw.rect(screen, (255, 255, 255), player2_input_rect)

                player1_surface = input_font.render(player1_name, True, (0, 0, 0))
                player2_surface = input_font.render(player2_name, True, (0, 0, 0))
                screen.blit(player1_surface, (player1_input_rect.x + 10, player1_input_rect.y + 10))
                screen.blit(player2_surface, (player2_input_rect.x + 10, player2_input_rect.y + 10))
                pygame.display.flip()


def Game_Handler(mode):


    if mode == "start_menu":

        # Update display based on mode selection
        GV.screen.blit(GV.background_image, (0, 0))
        GV.screen.blit(GV.Game_Name, (250, 50))
        GV.screen.blit(GV.back_arrow_img, (20, 20))
        
        #Draw Buttons
        pygame.draw.rect(GV.screen, (0, 0, 0), GV.human_vs_human_button)
        pygame.draw.rect(GV.screen, (0, 0, 0), GV.human_vs_computer_button)
        pygame.draw.rect(GV.screen, (0, 0, 0), GV.computer_vs_computer_button)

        #Add text to buttons
        GV.screen.blit(GV.human_vs_human_text, GV.human_vs_human_text_rect)
        GV.screen.blit(GV.human_vs_computer_text,GV.human_vs_computer_text_rect)
        GV.screen.blit(GV.computer_vs_computer_text, GV.computer_vs_computer_text_rect)
    
    elif mode == "Enter_Names":
        Enter_Names()
    
    elif mode == "human_vs_human":
        draw_game_board()
        Draw_Black_Gobblets()
        Draw_White_Gobblets()
        
    elif mode == "Computer_vs_Computer":
        draw_game_board()
        Draw_Black_Gobblets()
        Draw_White_Gobblets()
        pygame.display.set_caption("Game Started")
        #Handle the Game based on the difficulty of each AI
        if ai_1_difficulty == "hard" and ai_2_difficulty == "hard":
            #call the algorithm that handle this case
            print("hard vs hard")
        elif ai_1_difficulty == "easy" and ai_2_difficulty == "easy":
            #call the algorithm that handle this case
            print("easy vs easy")
        elif ai_1_difficulty == "easy" and ai_2_difficulty == "hard":
            #call the algorithm that handle this case
            print("easy vs hard")
        elif ai_1_difficulty == "hard" and ai_2_difficulty == "easy":
            #call the algorithm that handle this case
            print("hard vs easy")
            
  
    elif mode == "ai_vs_human_difficulty_selection":
        Difficulty_Selection()
    
    elif mode == "hard_ai_vs_human":
        draw_game_board()
        Draw_Black_Gobblets()
        Draw_White_Gobblets()
        pygame.display.set_caption("Game Started")
        
        
    elif mode == "easy_ai_vs_human":
        draw_game_board()
        Draw_Black_Gobblets()
        Draw_White_Gobblets()
        pygame.display.set_caption("Game Started")
    
    elif mode == "ai_1_difficulty_selection":
        
        Difficulty_Selection()
        pygame.display.set_caption("Difficulty Selection For Player 1 ")
    
    elif mode == "ai_2_difficulty_selection":

        Difficulty_Selection()
        pygame.display.set_caption("Difficulty Selection For Player 2 ")
        
    pygame.display.flip()
