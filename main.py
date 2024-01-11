from GUI import *

# Main function to run the game
if __name__ == "__main__":
    initialize_pygame()
    load_images()
    initialize_fonts()
    initialize_buttons()
    Events_Handler()
    game1.print_grid()
    pygame.quit()
    sys.exit()
