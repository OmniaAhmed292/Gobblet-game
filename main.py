'''Ideas about main

'''
from Game import Game
from Postion import Postion


# # Imports
# #import pygame
# from AIPlayer import AIPlayer
# from HumanPlayer import HumanPlayer
# from GameView import GameView



def main():
    game1 = Game("Hanan", "omnia")
    game1.print_grid()
    game1.do_turn(0, Postion(1, 1), from_pile=3)
    game1.print_grid()
    game1.do_turn(0, Postion(1, 2), from_pile=3)
    game1.print_grid()
    game1.do_turn(0, Postion(1, 2), from_grid=Postion(1, 1))
    game1.print_grid()
    game1.do_turn(0, Postion(1, 0), from_pile=2)
    game1.print_grid()

#     # Create classes
#     game_view = GameView()
#     ai_player = AIPlayer("black", difficulty=2)
#     human_player = HumanPlayer("white")
#
#     # Create game class to track state
#     game = Game()
#
#     # Select game mode
#     mode = input("Select game mode (1=human vs human, 2=human vs AI, 3=AI vs AI): ")
#
#     if mode == '1':
#         player1 = human_player
#         player2 = HumanPlayer("black")
#     elif mode == '2':
#         player1 = human_player
#         player2 = ai_player
#     else:
#         player1 = ai_player.clone("white")
#         player2 = ai_player
# # Game loop
#     current_player = player1
#
#
#     while True:
#
#         # Draw current game state
#         game_view.draw_board(game.board)
#         game_view.draw_pieces(game.pieces)
#
#         if current_player == ai_player:
#             # AI's turn
#             move = ai_player.get_move(game)
#             game.execute_move(move)
#             game_view.animate_move(move)
#
#         else:
#             # Human's turn
#             move = human_player.get_move(game)
#             if game.validate_move(move):
#                 game.execute_move(move)
#                 game_view.animate_move(move)
#
#         # Check end game conditions
#         if game.check_win(current_player):
#             game_view.show_game_over(current_player)
#             break
#
#         # Swap current player
#         if current_player == ai_player:
#             current_player = human_player
#         else:
#             current_player = ai_player
#
#     print("Game over! Winner:", winner)

if __name__ == "__main__":
    main()

