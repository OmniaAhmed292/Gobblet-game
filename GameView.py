import pygame

#Class that have everything about the game view
''' 
Gameview class is responsible for: 

* Handle user input events
* Render game board and pieces
* Animate moves
* Display game state and messages
* Allow player moves to be made
'''

class GameView:
    def __init__(self):
        self.screen = pygame.display.set_mode((400,400))
        pygame.display.set_caption("Gobblet")
        
        # Load images
        self.board_img = pygame.image.load("board.png") 
        self.white_pieces = [pygame.image.load("white1.png"), ...]
        self.black_pieces = [pygame.image.load("black1.png"), ...]
        
        # Game state
        self.board = [[None for _ in range(4)] for _ in range(4)]  
        self.current_player = "white"
        
    def draw(self):
        self.screen.blit(self.board_img, (0,0))  
        
        # Draw pieces onto board
        for r in range(4):
            for c in range(4):
                piece = self.board[r][c]
                if piece:
                    x, y = get_piece_coords(r, c)
                    self.screen.blit(piece.image, (x, y))
        
        pygame.display.update()
        
    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONUP:
                pos = pygame.mouse.get_pos()
                row, col = get_board_pos(pos)
                
                # Execute move...
        
    def update_status(self, text):
        # Render status text
        pass
        
    def get_spot_clicked(self, pos):
        # Convert click to row/col
        
    def highlight_moves(self, moves):
        # Highlight legal piece moves
        
    def animate_move(self, start, end):
        # Slide animation of piece  
        
    def update(self):
        # Update display / sprites
        
    def show_game_over(self, winner):  
        # Display game over message