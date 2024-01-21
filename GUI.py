import pygame
import sys
import os
import time
from Game import Game
from Logic import best_move, Random_move
from Position import Position
import time

# Initialize Pygame
def initialize_pygame():
    pygame.init()

    # Constants
    global WIDTH, HEIGHT, screen
    WIDTH, HEIGHT = 800, 600
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Gobblet Game")

    global turn
    turn = "P1"

    global ai_1_difficulty, ai_2_difficulty


# Load Images
def load_images():
    global background_image, back_arrow_img, black_gobblet_path, white_gobblet_path
    # Get the directory of the current script
    current_directory = os.path.dirname(__file__)
    # Define the relative path to the 'Images' folder
    image_directory = os.path.join(current_directory, 'Images')
    background_filename = "Background.png"
    back_arrow_filename = "back_arrow.png"
    black_gobblet_filename = "black_gobblet.png"
    white_gobblet_filename = "white_gobblet.png"

    # Define Images path
    background_path = os.path.join(image_directory, background_filename)
    back_arrow_path = os.path.join(image_directory, back_arrow_filename)
    black_gobblet_path = os.path.join(image_directory, black_gobblet_filename)
    white_gobblet_path = os.path.join(image_directory, white_gobblet_filename)

    # Load Background image and resize
    background_image = pygame.image.load(background_path)
    background_image = pygame.transform.scale(
        background_image, (WIDTH, HEIGHT))

    # Load Back arrow image and resize
    back_arrow_img = pygame.image.load(back_arrow_path)
    back_arrow_img = pygame.transform.scale(back_arrow_img, (40, 40))


# Initialize Fonts
def initialize_fonts():
    global Game_Name_font, Game_Name, button_font, difficulty_text_font, input_font
    global Player1_Turn_Text, Player1_Turn_Text_font
    global Player2_Turn_Text, Player2_Turn_Text_font

    Game_Name_font = pygame.font.Font(None, 60)
    Game_Name = Game_Name_font.render("Gobblet Game", True, (0, 0, 0))

    Player1_Turn_Text_font = pygame.font.Font(None, 35)
    Player1_Turn_Text = Player1_Turn_Text_font.render("Player 1 Turn", True, (0, 0, 0))

    Player2_Turn_Text_font = pygame.font.Font(None, 35)
    Player2_Turn_Text = Player2_Turn_Text_font.render("Player 2 Turn", True, (0, 0, 0))


# Initialize Buttons
def initialize_buttons():
    global human_vs_human_button, human_vs_computer_button, computer_vs_computer_button, back_button_rect, restart_button, quit_button
    global human_vs_human_text, human_vs_computer_text, computer_vs_computer_text, restart_text, quit_text
    global human_vs_human_text_rect, human_vs_computer_text_rect, computer_vs_computer_text_rect, restart_text_rect, quit_text_rect
    
    # difficulty buttons
    global hard_button, easy_button
    global hard_button_text, easy_button_text
    global hard_button_text_rect, easy_button_text_rect

    button_width = 250
    button_height = 50
    button_spacing = 20

    # Define buttons for difficulty selection screen
    button_width_difficulty = 200
    button_height_difficulty = 50
    difficulty_button_spacing = 20

    difficulty_button_y = (
        HEIGHT - ((button_height_difficulty + difficulty_button_spacing) * 3)) // 2

    total_button_height = (button_height * 3) + (button_spacing * 2)
    start_button_y = (HEIGHT - total_button_height) // 2

    human_vs_human_button = pygame.Rect(
        (WIDTH - button_width) // 2, start_button_y, button_width, button_height)
    human_vs_computer_button = pygame.Rect((WIDTH - button_width) // 2, start_button_y + button_height + button_spacing,
                                           button_width, button_height)
    computer_vs_computer_button = pygame.Rect((WIDTH - button_width) // 2,
                                              start_button_y +
                                              (button_height + button_spacing) *
                                              2, button_width,
                                              button_height)
    back_button_rect = pygame.Rect(20, 20, 40, 40)
    hard_button = pygame.Rect((WIDTH - button_width_difficulty) // 2, difficulty_button_y, button_width_difficulty,
                              button_height_difficulty)
    easy_button = pygame.Rect((WIDTH - button_width_difficulty) // 2,
                              difficulty_button_y + button_height_difficulty + difficulty_button_spacing,
                              button_width_difficulty, button_height_difficulty)
    
    restart_button = pygame.Rect((WIDTH - button_width_difficulty) // 2, difficulty_button_y, button_width_difficulty,
                              button_height_difficulty)
    quit_button = pygame.Rect((WIDTH - button_width_difficulty) // 2,
                              difficulty_button_y + button_height_difficulty + difficulty_button_spacing,
                              button_width_difficulty, button_height_difficulty)

    # Render text for buttons
    button_font = pygame.font.Font(None, 30)
    text_color = (255, 255, 255)

    human_vs_human_text = button_font.render(
        "Human vs Human", True, text_color)
    human_vs_computer_text = button_font.render(
        "Human vs Computer", True, text_color)
    computer_vs_computer_text = button_font.render(
        "Computer vs Computer", True, text_color)
    difficulty_text_font = pygame.font.Font(None, 30)
    hard_button_text = difficulty_text_font.render(
        "Hard", True, (255, 255, 255))
    easy_button_text = difficulty_text_font.render(
        "Easy", True, (255, 255, 255))
    restart_text = difficulty_text_font.render(
        "Restart", True, (255, 255, 255))
    quit_text = difficulty_text_font.render(
        "Quit", True, (255, 255, 255))

    # Get text rectangles for centering
    human_vs_human_text_rect = human_vs_human_text.get_rect(
        center=human_vs_human_button.center)
    human_vs_computer_text_rect = human_vs_computer_text.get_rect(
        center=human_vs_computer_button.center)
    computer_vs_computer_text_rect = computer_vs_computer_text.get_rect(
        center=computer_vs_computer_button.center)
    hard_button_text_rect = hard_button_text.get_rect(
        center=hard_button.center)
    easy_button_text_rect = easy_button_text.get_rect(
        center=easy_button.center)
    restart_text_rect = restart_text.get_rect(
        center=restart_button.center)
    quit_text_rect = quit_text.get_rect(
        center=quit_button.center)


def Game_Over():
    # Update display based on mode selection
    #screen.fill((220, 220, 220))
    # Update display based on mode selection
    screen.blit(background_image, (0, 0))
    global  input_font, WIDTH, HEIGHT
    text_font = pygame.font.Font(None, 100)
    Game_Over_text_surface = text_font.render("Game Over!", True, (200, 150, 50))
    # Get the rectangle of the text surface
    game_over_rect = Game_Over_text_surface.get_rect()

    # Center the text on the screen
    game_over_rect.center = ( WIDTH // 2,35)
    screen.blit(Game_Over_text_surface, game_over_rect)
    
    # Set the font and size for the winner player text
    winner_font = pygame.font.Font(None, 75)  

    # Create a text surface for the winner player text with black color
    winner_text_surface = winner_font.render(f"The winner is {winner}", True,(140, 180, 200))  # Black text color

    # Get the rectangle of the winner player text surface
    winner_rect = winner_text_surface.get_rect()

    # Center the winner player text below the "Game Over!" text
    winner_rect.midtop = (WIDTH // 2, game_over_rect.bottom + 50)

    # Blit the winner player text surface onto the screen
    screen.blit(winner_text_surface, winner_rect)
    
    # Draw Buttons
    pygame.draw.rect(screen, (0, 0, 0), restart_button)
    pygame.draw.rect(screen, (0, 0, 0), quit_button)

    # Add text to buttons
    screen.blit(restart_text, restart_text_rect)
    screen.blit(quit_text, quit_text_rect)
    
    
def Enter_Names():
        
    # Update display based on mode selection
    screen.blit(background_image, (0, 0))

    global player1_name, player2_name, active_input, Enter_Button_rect
    global player1_input_rect, player2_input_rect, input_font
    global player1_surface, player2_surface

    # Input fields for player names
    input_font = pygame.font.Font(None, 36)
    player1_input_rect = pygame.Rect((WIDTH - 400) // 2, (HEIGHT - 150) // 2, 400, 50)
    player2_input_rect = pygame.Rect((WIDTH - 400) // 2, (HEIGHT + 50) // 2, 400, 50)
    player1_name = ""
    player2_name = ""
    active_input = None
    

    # Draw input fields for player names
    pygame.draw.rect(screen, (255, 255, 255), player1_input_rect)
    pygame.draw.rect(screen, (255, 255, 255), player2_input_rect)

    player1_surface = input_font.render(player1_name, True, (0, 0, 0))
    player2_surface = input_font.render(player2_name, True, (0, 0, 0))
    screen.blit(player1_surface, (player1_input_rect.x + 10, player1_input_rect.y + 10))
    screen.blit(player2_surface, (player2_input_rect.x + 10, player2_input_rect.y + 10))

    # Text above input fields
    text_font = pygame.font.Font(None, 24)
    player1_text_surface = text_font.render("Player 1 Name:", True, (0, 0, 0))
    player2_text_surface = text_font.render("Player 2 Name:", True, (0, 0, 0))
    screen.blit(player1_text_surface, (player1_input_rect.x, player1_input_rect.y - 30))
    screen.blit(player2_text_surface, (player2_input_rect.x, player2_input_rect.y - 30))

    #Render text for buttons
    Enter_Button_Font = pygame.font.Font(None, 30)
    Text_Color = (255, 255, 255)

    #Enter Button
    Enter_Button_rect = pygame.Rect(500, 450, 200, 50)  
    Enter_Button_text = Enter_Button_Font.render("Enter Game", True, Text_Color)

    # Get text rectangles for centering
    Enter_Button_text_rect = Enter_Button_text.get_rect(center=Enter_Button_rect.center)


    #Draw Buttons
    pygame.draw.rect(screen, (0, 0, 0), Enter_Button_rect)


    #Add text to buttons
    screen.blit(Enter_Button_text, Enter_Button_text_rect)

def Difficulty_Selection():
    # Draw the buttons for difficulty selection screen
    pygame.draw.rect(screen, (0, 0, 0), hard_button)
    pygame.draw.rect(screen, (0, 0, 0), easy_button)
    # Update display based on mode selection
    screen.blit(background_image, (0, 0))
    screen.blit(back_arrow_img, (20, 20))

    # Draw Buttons
    pygame.draw.rect(screen, (0, 0, 0), hard_button)
    pygame.draw.rect(screen, (0, 0, 0), easy_button)

    # Add text to buttons
    screen.blit(hard_button_text, hard_button_text_rect)
    screen.blit(easy_button_text, easy_button_text_rect)


def draw_game_board():
    # Clear the screen
    # Fill the screen with white (change as needed)
    screen.fill((220, 220, 220))

    screen.blit(back_arrow_img, (20, 20))

    screen.blit(Game_Name, (250, 20))

    global board_width, board_offset_x, board_offset_y, square_size, grid_centers, square_center_x, square_center_y, Table_centers

    Table_centers = [[(0, 0) for _ in range(4)] for _ in range(4)]

    # Increase the grid size while keeping it centered
    # Adjust the board size according to the smaller screen dimension
    board_width = min(WIDTH, HEIGHT) // 1.5
    # Center the board horizontally
    board_offset_x = (WIDTH - board_width) // 2
    board_offset_y = (HEIGHT - board_width) // 2  # Center the board vertically
    square_size = board_width // 4  # Size of each square in the grid

    # 4x4 array representation of the grid
    # Initializing a 4x4 grid with (0, 0) coordinates
    grid_centers = [[(0, 0) for _ in range(4)] for _ in range(4)]

    # Define the alternating colors: orange and baby blue
    colors = [(255, 200, 100), (173, 216, 230)]

    # Draw a border around the grid
    border_color = (0, 0, 0)  # Define border color (black in this case)
    border_thickness = 4  # Adjust border thickness (in pixels)
    pygame.draw.rect(screen, border_color, (
        board_offset_x - border_thickness, board_offset_y -
        border_thickness, board_width + 2 * border_thickness,
        board_width + 2 * border_thickness), border_thickness)

    for x in range(4):
        for y in range(4):
            # Calculate the center of each square
            square_center_x = board_offset_x + x * square_size + square_size // 2
            square_center_y = board_offset_y + y * square_size + square_size // 2

            # Store the center coordinates in the grid
            grid_centers[x][y] = (square_center_x, square_center_y)
            Table_centers[x][y] = (
                grid_centers[x][y][0] - (square_size // 2), grid_centers[x][y][1] - (square_size // 2))

            # Alternate the color and draw each square
            color = colors[(x + y) % 2]
            pygame.draw.rect(screen, color, (
                board_offset_x + x * square_size, board_offset_y + y * square_size, square_size, square_size))

    # Draw the grid lines after coloring the squares
    for x in range(1, 4):
        pygame.draw.line(screen, (0, 0, 0), (board_offset_x + x * square_size, board_offset_y),
                         (board_offset_x + x * square_size, board_offset_y + board_width))
        pygame.draw.line(screen, (0, 0, 0), (board_offset_x, board_offset_y + x * square_size),
                         (board_offset_x + board_width, board_offset_y + x * square_size))

    if (turn == "P1"):
        screen.blit(Player1_Turn_Text, (300, 550))

    elif (turn == "P2"):
        screen.blit(Player2_Turn_Text, (300, 550))


def Black_Gobblets_Init_Positions():
    global Black_Gobblets_rect

    Black_Gobblets_rect = [[None for _ in range(4)] for _ in range(4)]

    for x in range(4):
        for y in range(3):
            Black_Gobblets_rect[x][y] = Black_Gobblets[x][y].get_rect()
            Black_Gobblets_rect[x][y].x = 80 + (x * 10)
            Black_Gobblets_rect[x][y].y = 100 + (x * 10) + (y * 100)


def Draw_Black_Gobblets():
    global Black_Gobblets
    Black_Gobblets = [[None for _ in range(4)] for _ in range(4)]

    for x in range(4):
        for y in range(3):
            Black_Gobblets[x][y] = pygame.image.load(black_gobblet_path)

    for i in range(4):
        Black_Gobblets[i][0] = pygame.transform.scale(
            Black_Gobblets[i][0], (100 - 20 * i, 100 - 20 * i))
        Black_Gobblets[i][1] = pygame.transform.scale(
            Black_Gobblets[i][1], (100 - 20 * i, 100 - 20 * i))
        Black_Gobblets[i][2] = pygame.transform.scale(
            Black_Gobblets[i][2], (100 - 20 * i, 100 - 20 * i))

    Black_Gobblets_Init_Positions()

    Display_Black_Gobblets()


def Display_Black_Gobblets():
    for x in range(4):
        for y in range(3):
            # Display the images on the screen
            screen.blit(Black_Gobblets[3 - x][2 - y],
                        Black_Gobblets_rect[3 - x][2 - y])


def White_Gobblets_Init_Positions():
    global White_Gobblets_rect

    White_Gobblets_rect = [[None for _ in range(4)] for _ in range(4)]

    for x in range(4):
        for y in range(3):
            White_Gobblets_rect[x][y] = White_Gobblets[x][y].get_rect()
            White_Gobblets_rect[x][y].x = 630 + (x * 10)
            White_Gobblets_rect[x][y].y = 100 + (x * 10) + (y * 100)


def Draw_White_Gobblets():
    global White_Gobblets
    White_Gobblets = [[None for _ in range(4)] for _ in range(4)]

    for x in range(4):
        for y in range(3):
            White_Gobblets[x][y] = pygame.image.load(white_gobblet_path)

    for i in range(4):
        White_Gobblets[i][0] = pygame.transform.scale(
            White_Gobblets[i][0], (115 - 20 * i, 115 - 20 * i))
        White_Gobblets[i][1] = pygame.transform.scale(
            White_Gobblets[i][1], (115 - 20 * i, 115 - 20 * i))
        White_Gobblets[i][2] = pygame.transform.scale(
            White_Gobblets[i][2], (115 - 20 * i, 115 - 20 * i))

    White_Gobblets_Init_Positions()

    Display_White_Gobblets()

    pygame.display.flip()


def Display_White_Gobblets():
    for x in range(4):
        for y in range(3):
            # Display the images on the screen
            screen.blit(White_Gobblets[3 - x][2 - y],
                        White_Gobblets_rect[3 - x][2 - y])


def Display_Gobblets():
    for x in range(4):
        for y in range(3):
            # Display the images on the screen
            screen.blit(White_Gobblets[3 - x][2 - y],
                        White_Gobblets_rect[3 - x][2 - y])
            screen.blit(Black_Gobblets[3 - x][2 - y],
                        Black_Gobblets_rect[3 - x][2 - y])

    pygame.display.flip()


def move_gobblet(Gobblet_rect, grid_centers_tuple):
    draw_game_board()

    for x in range(4):
        for y in range(3):

            if (Gobblet_rect == Black_Gobblets_rect[x][y]):
                Black_Gobblets_rect[x][y].x = grid_centers_tuple[0] + x * 10
                Black_Gobblets_rect[x][y].y = grid_centers_tuple[1] + x * 10

                Display_Gobblets()

            elif (Gobblet_rect == White_Gobblets_rect[x][y]):

                if (x == 0):
                    White_Gobblets_rect[x][y].x = grid_centers_tuple[0] - 7
                    White_Gobblets_rect[x][y].y = grid_centers_tuple[1] - 7

                elif (x == 1):
                    White_Gobblets_rect[x][y].x = grid_centers_tuple[0] + 4
                    White_Gobblets_rect[x][y].y = grid_centers_tuple[1] + 4

                elif (x == 2):
                    White_Gobblets_rect[x][y].x = grid_centers_tuple[0] + 11
                    White_Gobblets_rect[x][y].y = grid_centers_tuple[1] + 11

                elif (x == 3):
                    White_Gobblets_rect[x][y].x = grid_centers_tuple[0] + 22
                    White_Gobblets_rect[x][y].y = grid_centers_tuple[1] + 22

                Display_Gobblets()

    pygame.display.flip()


def Move_Human_Goblet():
    global selected_image, turn, pile_no, game1, mode_selection
    clicked = False

    # First click: select the image
    mouse_pos = pygame.mouse.get_pos()

    do_turn_from = Position(None, None)
    do_turn_to = Position(None, None)
  
    i = None
    j = None

    
    for x in range (4):

        if(mouse_pos[0] < 200 or mouse_pos[0] > 600 or mouse_pos[1] < 100 or mouse_pos[1] > 500):
            do_turn_from.x = None
            do_turn_from.y = None
            pass

        else:
            if(mouse_pos[0] > (200 + x * 100) and mouse_pos[0] < (200 + (x + 1) * 100)):
                i = x
                do_turn_from.y = x

            if(mouse_pos[1] > (100 + x * 100) and mouse_pos[1] < (100 + (x + 1) * 100)):
                j = x
                do_turn_from.x = x

    for x in range(4):
        for y in range(3):

            if (mode_selection == "human_vs_human"):

                if (turn == "P1"):
                    if (Black_Gobblets_rect[3 - x][2 - y].collidepoint(mouse_pos)):
                        selected_image = Black_Gobblets_rect[3 - x][2 - y]
                        pile_no = (2 - y)
                        clicked = True

                elif (turn == "P2"):
                    if (White_Gobblets_rect[3 - x][2 - y].collidepoint(mouse_pos)):
                        selected_image = White_Gobblets_rect[3 - x][2 - y]
                        pile_no = (2 - y)
                        clicked = True

            elif (mode_selection == "hard_ai_vs_human"):

                if (turn == "P1"):
                    if (Black_Gobblets_rect[3 - x][2 - y].collidepoint(mouse_pos)):
                        selected_image = Black_Gobblets_rect[3 - x][2 - y]
                        pile_no = (2 - y)
                        clicked = True

                elif (turn == "P2"):
                    return

            elif (mode_selection == "easy_ai_vs_human"):

                if (turn == "P1"):
                    if (Black_Gobblets_rect[3 - x][2 - y].collidepoint(mouse_pos)):
                        selected_image = Black_Gobblets_rect[3 - x][2 - y]
                        pile_no = (2 - y)
                        clicked = True

                elif (turn == "P2"):
                    return

    while clicked == True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            elif event.type == pygame.MOUSEBUTTONDOWN and clicked:
                # Second click: move the image
                mouse_pos = pygame.mouse.get_pos()
                # minimum = math.sqrt(Table_centers[0][0][0] ** 2 + Table_centers[0][0][1] ** 2)
                i = 0
                j = 0

                for x in range(4):

                    if (mouse_pos[0] > (200 + x * 100) and mouse_pos[0] < (200 + (x + 1) * 100)):
                        i = x

                    if (mouse_pos[1] > (100 + x * 100) and mouse_pos[1] < (100 + (x + 1) * 100)):
                        j = x

                if selected_image:

                    global game1

                    if (turn == "P1"):
                        turn = "P2"
                        draw_game_board()
                        move_gobblet(selected_image, Table_centers[i][j])
                        game1.do_turn(0, Position(j, i), from_pile=pile_no)
                        var1, var2 = game1.check_win()
                        print(var1, var2)

                    elif (turn == "P2"):
                        turn = "P1"
                        draw_game_board()
                        move_gobblet(selected_image, Table_centers[i][j])
                        game1.do_turn(1, Position(j, i), from_pile=pile_no)
                        var1, var2 = game1.check_win()
                        print(var1, var2)

                    game1.print_grid()

                    clicked = False
                    selected_image = None

    #if (turn == "P1"):
    #    turn = "P2"

    #elif (turn == "P2"):
    #    turn = "P1"
    # Inside Move_Human_Goblet() after making the move:
    var1, var2 = game1.check_win()
    if var1:  # Assuming var1 indicates a win condition
        mode_selection = "game_over"
        global winner
        winner = "Player 1" if turn == "P2" else "Player 2"
        Game_Handler(mode_selection)
        print(f"{winner} wins!")

# Main Game Loop
def Events_Handler():
    # Game Mode Variables
    global mode_selection, previous_mode, game_type

    # Enter Names Global Variables
    global active_input, player1_name, player2_name, player1_input_rect, player2_input_rect

    global ai_1_difficulty, ai_2_difficulty


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
                        mode_selection = "Enter_Names"  # Transition to Enter names mode
                        Game_Handler(mode_selection)
                    elif human_vs_computer_button.collidepoint(event.pos):
                        previous_mode = mode_selection
                        # Transition to Human vs Computer Difficulty selection mode
                        mode_selection = "ai_vs_human_difficulty_selection"
                        print("Entered Human V Computer Difficulty Selection mode")
                        Game_Handler(mode_selection)
                    elif computer_vs_computer_button.collidepoint(event.pos):
                        previous_mode = mode_selection
                        # Transition to Computer vs Computer Difficulty selection mode
                        mode_selection = "ai_1_difficulty_selection"
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

                elif mode_selection == "human_vs_human":
                    Move_Human_Goblet()

                elif  mode_selection == "hard_ai_vs_human":
                    Move_Human_Goblet()
                    mode_selection = "hard_ai_vs_human"
                    Game_Handler(mode_selection)

                elif mode_selection == "easy_ai_vs_human":
                    Move_Human_Goblet()
                    mode_selection = "easy_ai_vs_human"
                    Game_Handler(mode_selection)
                                   
                elif mode_selection == "game_over":
                   if restart_button.collidepoint(event.pos):
                        
                        previous_mode = mode_selection  # Assign previous mode before changing
                        mode_selection = "start_menu"
                        Game_Handler(mode_selection)

                   elif quit_button.collidepoint(event.pos):
                        pygame.quit()
                        sys.exit()
                   
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

                player1_surface = input_font.render(
                    player1_name, True, (0, 0, 0))
                player2_surface = input_font.render(
                    player2_name, True, (0, 0, 0))
                screen.blit(
                    player1_surface, (player1_input_rect.x + 10, player1_input_rect.y + 10))
                screen.blit(
                    player2_surface, (player2_input_rect.x + 10, player2_input_rect.y + 10))
                pygame.display.flip()

flag=1

def Game_Handler(mode):
    global ai_1_difficulty, ai_2_difficulty
    global game1
    global turn
    global mode_selection
    global flag

    if mode == "start_menu":

        # Update display based on mode selection
        screen.blit(background_image, (0, 0))
        screen.blit(Game_Name, (250, 50))
        screen.blit(back_arrow_img, (20, 20))

        # Draw Buttons
        pygame.draw.rect(screen, (0, 0, 0), human_vs_human_button)
        pygame.draw.rect(screen, (0, 0, 0), human_vs_computer_button)
        pygame.draw.rect(screen, (0, 0, 0), computer_vs_computer_button)

        # Add text to buttons
        screen.blit(human_vs_human_text, human_vs_human_text_rect)
        screen.blit(human_vs_computer_text, human_vs_computer_text_rect)
        screen.blit(computer_vs_computer_text, computer_vs_computer_text_rect)

    elif mode == "Enter_Names":
        Enter_Names()
    elif mode == "human_vs_human":
        draw_game_board()
        pygame.display.flip()
        Draw_Black_Gobblets()
        Draw_White_Gobblets()
        
        game1 = Game(player1_name, player2_name)
        pygame.display.flip()
        
        '''
        end = False
        while not end:
            end, winner = game1.check_win()
            if end:
                break
            # Handle player turns and game logic here
        '''


    elif mode == "Computer_vs_Computer":
        draw_game_board()
        Draw_Black_Gobblets()
        Draw_White_Gobblets()
        pygame.display.flip()

        #global game1
        game1 = Game("player1_name", "player2_name")

        pygame.display.set_caption("Game Started")
        # Handle the Game based on the difficulty of each AI
        if ai_1_difficulty == "hard" and ai_2_difficulty == "hard":
            # call the algorithm that handle this case
            print("hard vs hard")

            end = False
            while not end:
                global winner
                end, winner = game1.check_win()
                to, frm, pile, pn, sz = best_move(game1, True, 0)
                game1.do_turn(0, to, frm, pile)
                turn = "P2"
                draw_game_board()
                move_gobblet(
                    Black_Gobblets_rect[4 - sz][pn], Table_centers[to.y][to.x])
                game1.print_grid()

                end, winner = game1.check_win()
                print(end, winner)
                if end:  # Assuming var1 indicates a win condition
                    mode_selection = "game_over"
                    
                    winner = "Player 1" if turn == "P2" else "Player 2"
                    Game_Handler(mode_selection)
                    print(f"{winner} wins!")
                    return

                to, frm, pile, pn, sz = best_move(game1, False, 1)
                game1.do_turn(1, to, frm, pile)
                turn = "P1"
                draw_game_board()
                move_gobblet(
                    White_Gobblets_rect[4 - sz][pn], Table_centers[to.y][to.x])
                game1.print_grid()
                
                end, winner = game1.check_win()
                print(end, winner)
                
                if end:  # Assuming var1 indicates a win condition
                    mode_selection = "game_over"
                    
                    winner = "Player 1" if turn == "P2" else "Player 2"
                    Game_Handler(mode_selection)
                    print(f"{winner} wins!")
                    return

        elif ai_1_difficulty == "easy" and ai_2_difficulty == "easy":
            end = False
            while not end:
                end, winner = game1.check_win()
                to, frm, pile, pn, sz = Random_move(game1, 0)
                game1.do_turn(0, to, frm, pile)
                turn = "P2"
                draw_game_board()
                move_gobblet(
                    Black_Gobblets_rect[4 - sz][pn], Table_centers[to.y][to.x])
                game1.print_grid()
                time.sleep(2)
                # move_gobblet(Black_Gobblets_rect[1][0], Table_centers[to.x][to.y])

                end, winner = game1.check_win()
                print(end, winner)
                if end:  # Assuming var1 indicates a win condition
                    mode_selection = "game_over"
                    
                    winner = "Player 1" if turn == "P2" else "Player 2"
                    Game_Handler(mode_selection)
                    print(f"{winner} wins!")
                    return

                turn = "P1"
                draw_game_board()
                to, frm, pile, pn, sz = Random_move(game1, 1)
                game1.do_turn(1, to, frm, pile)
                move_gobblet(
                    White_Gobblets_rect[4 - sz][pn], Table_centers[to.y][to.x])
                game1.print_grid()
                time.sleep(2)
                end, winner = game1.check_win()
                print(end, winner)
                if end:  # Assuming var1 indicates a win condition
                    mode_selection = "game_over"
                    
                    winner = "Player 1" if turn == "P2" else "Player 2"
                    Game_Handler(mode_selection)
                    print(f"{winner} wins!")
                    return
            # call the algorithm that handle this case
            print("easy vs easy")
        elif ai_1_difficulty == "easy" and ai_2_difficulty == "hard":
            # call the algorithm that handle this case
            end = False
            while not end:
                end, winner = game1.check_win()
                to, frm, pile, pn, sz = Random_move(game1, 0)
                time.sleep(2)
                game1.do_turn(0, to, frm, pile)
                turn = "P2"
                draw_game_board()
                move_gobblet(
                    Black_Gobblets_rect[4 - sz][pn], Table_centers[to.y][to.x])
                game1.print_grid()

                end, winner = game1.check_win()
                print(end, winner)
                if end:  # Assuming var1 indicates a win condition
                    mode_selection = "game_over"
                    
                    winner = "Player 1" if turn == "P2" else "Player 2"
                    Game_Handler(mode_selection)
                    print(f"{winner} wins!")
                    return

                # move_gobblet(Black_Gobblets_rect[1][0], Table_centers[to.x][to.y])

                to, frm, pile, pn, sz = best_move(game1, True, 1)
                game1.do_turn(1, to, frm, pile)
                turn = "P1"
                draw_game_board()
                move_gobblet(
                    White_Gobblets_rect[4 - sz][pn], Table_centers[to.y][to.x])
                game1.print_grid()
                end, winner = game1.check_win()
                print(end, winner)

                if end:  # Assuming var1 indicates a win condition
                    mode_selection = "game_over"
                    
                    winner = "Player 1" if turn == "P2" else "Player 2"
                    Game_Handler(mode_selection)
                    print(f"{winner} wins!")
                    return

            print("easy vs hard")
        elif ai_1_difficulty == "hard" and ai_2_difficulty == "easy":
            # call the algorithm that handle this case
            end = False
            while not end:
                end, winner = game1.check_win()
                to, frm, pile, pn, sz = best_move(game1, False, 0)
                game1.do_turn(0, to, frm, pile)
                turn = "P2"
                draw_game_board()
                move_gobblet(
                    Black_Gobblets_rect[4 - sz][pn], Table_centers[to.y][to.x])
                game1.print_grid()
                
                end, winner = game1.check_win()
                print(end, winner)
                if end:  # Assuming var1 indicates a win condition
                    mode_selection = "game_over"
                    
                    winner = "Player 1" if turn == "P2" else "Player 2"
                    Game_Handler(mode_selection)
                    print(f"{winner} wins!")
                    return

                # move_gobblet(Black_Gobblets_rect[1][0], Table_centers[to.x][to.y])

                to, frm, pile, pn, sz = Random_move(game1, 1)
                time.sleep(2)
                game1.do_turn(1, to, frm, pile)
                turn = "P2"
                draw_game_board()
                move_gobblet(
                    White_Gobblets_rect[4 - sz][pn], Table_centers[to.y][to.x])
                game1.print_grid()
                end, winner = game1.check_win()
                print(end, winner)

                if end:  # Assuming var1 indicates a win condition
                    mode_selection = "game_over"
                    
                    winner = "Player 1" if turn == "P2" else "Player 2"
                    Game_Handler(mode_selection)
                    print(f"{winner} wins!")
                    return
            print("hard vs easy")

    elif mode == "ai_vs_human_difficulty_selection":
        Difficulty_Selection()

    elif mode == "hard_ai_vs_human":
        if(flag==1):
            draw_game_board()
            Draw_Black_Gobblets()
            Draw_White_Gobblets()
            game1 = Game("player1_name", "player2_name")
            pygame.display.flip()
            pygame.display.set_caption("Game Started")
            flag=0
            end=False

        # Handle the Game with AI Hard and Human
        print("hard vs human")
        if(turn=="P2"):
            to, frm, pile, pn, sz = best_move(game1, True, 1)
            game1.do_turn(1, to, frm, pile)
            turn = "P1"
            draw_game_board()
            move_gobblet(
                White_Gobblets_rect[4 - sz][pn], Table_centers[to.y][to.x])
            game1.print_grid()
            end, winner = game1.check_win()
            print(end, winner)

            if end:  # Assuming var1 indicates a win condition
                mode_selection = "game_over"
                flag=1
                winner = "Player 1" if turn == "P2" else "Player 2"
                Game_Handler(mode_selection)
                print(f"{winner} wins!")
                
                return

        
      

    elif mode == "easy_ai_vs_human":
        if(flag==1):
            draw_game_board()
            Draw_Black_Gobblets()
            Draw_White_Gobblets()
            game1 = Game("player1_name", "player2_name")
            pygame.display.flip()
            pygame.display.set_caption("Game Started")
            flag=0
            end=False

        # Handle the Game with AI Hard and Human
        print("Easy vs human")
        if(turn=="P2"):
            to, frm, pile, pn, sz = Random_move(game1, 1)
            game1.do_turn(1, to, frm, pile)
            turn = "P1"
            draw_game_board()
            move_gobblet(
                White_Gobblets_rect[4 - sz][pn], Table_centers[to.y][to.x])
            game1.print_grid()
            end, winner = game1.check_win()
            print(end, winner)

            if end:  # Assuming var1 indicates a win condition
                mode_selection = "game_over"
                flag=1
                winner = "Player 1" if turn == "P2" else "Player 2"
                Game_Handler(mode_selection)
                print(f"{winner} wins!")
                
                return


    elif mode == "ai_1_difficulty_selection":

        Difficulty_Selection()
        pygame.display.set_caption("Difficulty Selection For Player 1 ")

    elif mode == "ai_2_difficulty_selection":

        Difficulty_Selection()
        pygame.display.set_caption("Difficulty Selection For Player 2 ")
        
    elif mode == "game_over":
        pygame.display.set_caption("Game Over!")
        Game_Over()

            

    pygame.display.flip()
