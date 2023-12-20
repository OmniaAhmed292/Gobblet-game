import pygame
import sys
import os
import math
from Game import Game
from Postion import Postion
#GUI
from Draw_Gobblets import *
from EventHandling import *
import Global_variables as GV

#Handle things about game options and initializations 

def initialize_pygame():
    pygame.init()
    # Constants
    GV.WIDTH, GV.HEIGHT = 800, 600
    GV.screen = pygame.display.set_mode((GV.WIDTH, GV.HEIGHT))
    pygame.display.set_caption("Gobblet Game")

    GV.turn = "P1"
    



# Initialize Buttons
def initialize_buttons():
   

    button_width = 250
    button_height = 50
    button_spacing = 20

    # Define buttons for difficulty selection screen
    button_width_difficulty = 200
    button_height_difficulty = 50
    difficulty_button_spacing = 20

    difficulty_button_y = (GV.HEIGHT - ((button_height_difficulty + difficulty_button_spacing) * 3)) // 2

    total_button_height = (button_height * 3) + (button_spacing * 2)
    start_button_y = (GV.HEIGHT - total_button_height) // 2

    GV.human_vs_human_button = pygame.Rect((GV.WIDTH - button_width) // 2, start_button_y, button_width, button_height)
    GV.human_vs_computer_button = pygame.Rect((GV.WIDTH - button_width) // 2, start_button_y + button_height + button_spacing, button_width, button_height)
    GV.computer_vs_computer_button = pygame.Rect((GV.WIDTH - button_width) // 2, start_button_y + (button_height + button_spacing) * 2, button_width, button_height)
    GV.back_button_rect = pygame.Rect(20, 20, 40, 40)
    GV.hard_button = pygame.Rect((GV.WIDTH - button_width_difficulty) // 2, difficulty_button_y, button_width_difficulty, button_height_difficulty)
    GV.easy_button = pygame.Rect((GV.WIDTH - button_width_difficulty) // 2, difficulty_button_y + button_height_difficulty + difficulty_button_spacing, button_width_difficulty, button_height_difficulty)

    #Render text for buttons
    button_font = pygame.font.Font(None, 30)
    text_color = (255, 255, 255)

    GV.human_vs_human_text = button_font.render("Human vs Human", True, text_color)
    GV.human_vs_computer_text = button_font.render("Human vs Computer", True, text_color)
    GV.computer_vs_computer_text = button_font.render("Computer vs Computer", True, text_color)
    GV.difficulty_text_font = pygame.font.Font(None, 30)
    GV.hard_button_text = GV.difficulty_text_font.render("Hard", True, (255, 255, 255))
    GV.easy_button_text = GV.difficulty_text_font.render("Easy", True, (255, 255, 255))

    # Get text rectangles for centering
    GV.human_vs_human_text_rect = GV.human_vs_human_text.get_rect(center=GV.human_vs_human_button.center)
    GV.human_vs_computer_text_rect = GV.human_vs_computer_text.get_rect(center=GV.human_vs_computer_button.center)
    GV.computer_vs_computer_text_rect = GV.computer_vs_computer_text.get_rect(center=GV.computer_vs_computer_button.center)
    GV.hard_button_text_rect = GV.hard_button_text.get_rect(center=GV.hard_button.center)
    GV.easy_button_text_rect = GV.easy_button_text.get_rect(center=GV.easy_button.center)


# Initialize Fonts
def initialize_fonts():
   
    GV.Game_Name_font = pygame.font.Font(None, 60)
    GV.Game_Name = GV.Game_Name_font.render("Gobblet Game", True, (0, 0, 0))

    GV.Player1_Turn_Text_font = pygame.font.Font(None, 35)
    GV.Player1_Turn_Text = GV.Player1_Turn_Text_font.render("Player 1 Turn", True, (0, 0, 0))

    GV.Player2_Turn_Text_font = pygame.font.Font(None, 35)
    GV.Player2_Turn_Text = GV.Player2_Turn_Text_font.render("Player 2 Turn", True, (0, 0, 0))



# Load Images
def load_images():
    
    # Get the directory of the current script
    current_directory = os.path.dirname(__file__)
    # Define the relative path to the 'Images' folder
    image_directory = os.path.join(current_directory, 'Images')
    background_filename = "background.png"
    back_arrow_filename = "back_arrow.png"
    
    
    # Define Images path
    background_path = os.path.join(image_directory, background_filename)
    back_arrow_path = os.path.join(image_directory, back_arrow_filename)
    
    
    # Load Background image and resize
    GV.background_image = pygame.image.load(background_path)
    GV.background_image = pygame.transform.scale(GV.background_image, (GV.WIDTH, GV.HEIGHT))
    
    # Load Back arrow image and resize
    GV.back_arrow_img = pygame.image.load(back_arrow_path)
    GV.back_arrow_img = pygame.transform.scale(GV.back_arrow_img, (40, 40))


def Enter_Names():
        
    # Update display based on mode selection
    GV.screen.blit(GV.background_image, (0, 0))

  

    # Input fields for player names
    GV.input_font = pygame.font.Font(None, 36)
    GV.player1_input_rect = pygame.Rect((WIDTH - 400) // 2, (HEIGHT - 150) // 2, 400, 50)
    GV.player2_input_rect = pygame.Rect((WIDTH - 400) // 2, (HEIGHT + 50) // 2, 400, 50)
    GV.player1_name = ""
    GV.player2_name = ""
    GV.active_input = None
    

    # Draw input fields for player names
    pygame.draw.rect(screen, (255, 255, 255), player1_input_rect)
    pygame.draw.rect(screen, (255, 255, 255), player2_input_rect)

    GV.player1_surface = input_font.render(player1_name, True, (0, 0, 0))
    GV.player2_surface = input_font.render(player2_name, True, (0, 0, 0))
    screen.blit(GV.player1_surface, (GV.player1_input_rect.x + 10, GV.player1_input_rect.y + 10))
    screen.blit(GV.player2_surface, (GV.player2_input_rect.x + 10, GV.player2_input_rect.y + 10))

    # Text above input fields
    GV.text_font = pygame.font.Font(None, 24)
    GV.player1_text_surface = text_font.render("Player 1 Name:", True, (0, 0, 0))
    GV.player2_text_surface = text_font.render("Player 2 Name:", True, (0, 0, 0))
    GV.screen.blit(player1_text_surface, (GV.player1_input_rect.x, GV.player1_input_rect.y - 30))
    screen.blit(GV.player2_text_surface, (GV.player2_input_rect.x, GV.player2_input_rect.y - 30))

    #Render text for buttons
    Enter_Button_Font = pygame.font.Font(None, 30)
    Text_Color = (255, 255, 255)

    #Enter Button
    GV.Enter_Button_rect = pygame.Rect(500, 450, 200, 50)  
    GV.Enter_Button_text = Enter_Button_Font.render("Enter Game", True, Text_Color)

    # Get text rectangles for centering
    GV.Enter_Button_text_rect = Enter_Button_text.get_rect(center=GV.Enter_Button_rect.center)


    #Draw Buttons
    pygame.draw.rect(screen, (0, 0, 0), GV.Enter_Button_rect)


    #Add text to buttons
    GV.screen.blit(GV.Enter_Button_text, GV.Enter_Button_text_rect)


def Difficulty_Selection():
        # Draw the buttons for difficulty selection screen
        pygame.draw.rect(GV.screen, (0, 0, 0), GV.hard_button)
        pygame.draw.rect(GV.screen, (0, 0, 0), GV.easy_button)
        # Update display based on mode selection
        GV.screen.blit(GV.background_image, (0, 0))
        GV.screen.blit(GV.back_arrow_img, (20, 20))

        #Draw Buttons
        pygame.draw.rect(GV.screen, (0, 0, 0), GV.hard_button)
        pygame.draw.rect(GV.screen, (0, 0, 0), GV.easy_button)

        #Add text to buttons
        GV.screen.blit(GV.hard_button_text, GV.hard_button_text_rect)
        GV.screen.blit(GV.easy_button_text, GV.easy_button_text_rect)
    



def draw_game_board():
    
    # Clear the screen
    GV.screen.fill((220, 220, 220)) 

    GV.screen.blit(GV.back_arrow_img, (20, 20))

    GV.screen.blit(Game_Name, (250, 20))

    
    GV.Table_centers = [[(0, 0) for _ in range(4)] for _ in range(4)]

    # Increase the grid size while keeping it centered
    GV.board_width = min(GV.WIDTH, GV.HEIGHT) // 1.5  # Adjust the board size according to the smaller screen dimension
    GV.board_offset_x = (GV.WIDTH - GV.board_width) // 2  # Center the board horizontally
    GV.board_offset_y = (GV.HEIGHT - GV.board_width) // 2  # Center the board vertically
    GV.square_size = GV.board_width // 4  # Size of each square in the grid
    
    # 4x4 array representation of the grid
    GV.grid_centers = [[(0, 0) for _ in range(4)] for _ in range(4)]  # Initializing a 4x4 grid with (0, 0) coordinates
    
    colors = [(255, 200, 100), (173, 216, 230)]  # Define the alternating colors: orange and baby blue
    
    # Draw a border around the grid
    border_color = (0, 0, 0)  # Define border color (black in this case)
    border_thickness = 4  # Adjust border thickness (in pixels)
    pygame.draw.rect(GV.screen, border_color, (board_offset_x - border_thickness, board_offset_y - border_thickness, board_width + 2 * border_thickness, board_width + 2 * border_thickness), border_thickness)
    
    for x in range(4):
        for y in range(4):
            # Calculate the center of each square
            square_center_x = board_offset_x + x * square_size + square_size // 2
            square_center_y = board_offset_y + y * square_size + square_size // 2
            
            # Store the center coordinates in the grid
            grid_centers[x][y] = (square_center_x, square_center_y)
            Table_centers[x][y] = (grid_centers[x][y][0] - (square_size // 2), grid_centers[x][y][1] - (square_size // 2))
            
            # Alternate the color and draw each square
            color = colors[(x + y) % 2]
            pygame.draw.rect(GV.screen, color, (GV.board_offset_x + x * square_size, GV.board_offset_y + y * square_size, square_size, square_size))
    
    # Draw the grid lines after coloring the squares
    for x in range(1, 4):
        pygame.draw.line(screen, (0, 0, 0), (board_offset_x + x * square_size, board_offset_y),
                         (board_offset_x + x * square_size, board_offset_y + board_width))
        pygame.draw.line(screen, (0, 0, 0), (board_offset_x, board_offset_y + x * square_size),
                         (board_offset_x + board_width, board_offset_y + x * square_size))


    if(turn == "P2"):
        GV.screen.blit(GV.Player1_Turn_Text, (300, 550))

    elif(turn == "P1"):
       GV.screen.blit(GV.Player2_Turn_Text, (300, 550))
      