from os import environ
# Hide the pygame support prompt (must be before pygame import)
environ['PYGAME_HIDE_SUPPORT_PROMPT'] = '1'
import argparse
import pygame
import chess
import timeit

from graphics import *
from ai import *

CLOCK_RATE = 60

# Holds blue dots that show potential moves from the user's selected piece
potentialMoves = []

def main():
   parser = argparse.ArgumentParser(prog='python3 engine.py', description='Play chess against an AI or watch 2 AIs play against each other')
   parser.add_argument('--ai', '-a', action='store_true', help='Instead of playing against AI, pin 2 of them against each other and watch them play')
   parser.add_argument('--color', '-c', default='white', help='Choose the color on the bottom of the screen (white or black)')
   parser.add_argument('--heuristic', default='pieceCount', help="Choose the AI's method of evaluating the board state. Options: pieceCount, random, worstPossibleMove")
   args = parser.parse_args()
   
   if args.color.lower() not in ['white', 'black']:
      parser.print_help()
      print('')
      print('Invalid color argument. Must be either white or black')
      return
   if args.heuristic.lower() not in ['piececount', 'random', 'worstpossiblemove']:
      parser.print_help()
      print('')
      print('Invalid heuristic argument. Must be either pieceCount, random, or worstPossibleMove')
      return

   # Initialize pygame
   pygame.init()
   
   # Create objects for each block on the board
   initBoardGraphics()
   
   # Set up checkers game
   game = chess.Board()
   
   # Define colors
   if args.color.lower() == 'white':
      userColor = chess.WHITE
      aiColor = chess.BLACK
   else:
      userColor = chess.BLACK
      aiColor = chess.WHITE

   # Initialize AI
   if args.ai:
      ai1 = chessAI(chess.WHITE, heuristic=args.heuristic)
      ai2 = chessAI(chess.BLACK, heuristic=args.heuristic)
   else:
      ai = chessAI(aiColor, heuristic=args.heuristic)

   # Set up game window
   screen = pygame.display.set_mode([WINDOW_WIDTH, WINDOW_HEIGHT])
   pygame.display.set_caption('Chess')

   # Initialize clock
   clock = pygame.time.Clock()

   # Loop until the window is closed by the user
   numIterations = 0
   loop = True
   while loop and not game.is_game_over(claim_draw=True):
      # Check for input
      for event in pygame.event.get():
         if event.type == pygame.MOUSEBUTTONDOWN:
            clickHandler(game, pygame.mouse.get_pos(), userColor)
         elif event.type == pygame.QUIT:
            loop = False
      
      # Draw checkered background
      drawBackground(screen)
      
      # Draw in pieces found on the board
      for square in chess.SQUARES:
         piece = game.piece_at(square)
         if piece != None:
            (row, col) = squareToDisplayRowCol(square, userColor)
            drawPieceInSquare(screen, piece, row, col)

      # Draw in the potential moves
      drawPotentialMoves(screen, potentialMoves, userColor)

      # Update the screen
      pygame.display.update()

      # AI's turn
      if args.ai:
         if game.turn == chess.WHITE:
            start = timeit.default_timer()
            bestMove = ai1.minimax(game, depth=3)
            print(str(timeit.default_timer() - start) + ' seconds')
            if bestMove in game.legal_moves:
               game.push(bestMove)
            else:
               if not game.is_game_over():
                  print('AI tried to make illegal move ' + str(bestMove))
               break
         elif game.turn == chess.BLACK:
            start = timeit.default_timer()
            bestMove = ai2.minimax(game, depth=3)
            print(str(timeit.default_timer() - start) + ' seconds')
            if bestMove in game.legal_moves:
               game.push(bestMove)
            else:
               if not game.is_game_over():
                  print('AI tried to make illegal move ' + str(bestMove))
               break
      elif game.turn == aiColor:
         start = timeit.default_timer()
         bestMove = ai.minimax(game, depth=3)
         print(str(timeit.default_timer() - start) + ' seconds')
         if bestMove in game.legal_moves:
            game.push(bestMove)
         else:
            if not game.is_game_over():
               print('AI tried to make illegal move ' + str(bestMove))
            break
               
      # Ensure the game doesn't run faster than CLOCK_RATE fps
      clock.tick(CLOCK_RATE)
      numIterations += 1
   
   # Opposite of pygame.init()
   pygame.quit()

   outcome = game.outcome(claim_draw=True)
   if outcome is not None:
      if outcome.termination == chess.Termination.CHECKMATE:
         winner = 'White' if outcome.winner == True else 'Black'
         print(f'{winner} wins with checkmate!')
      elif outcome.termination == chess.Termination.STALEMATE:
         print('Draw - Stalemate!')
      elif outcome.termination == chess.Termination.INSUFFICIENT_MATERIAL:
         print('Draw - Insufficient material!')
      elif outcome.termination == chess.Termination.FIFTY_MOVES:
         print('Draw - 50 moves without a capture or pawn move!')
      elif outcome.termination == chess.Termination.SEVENTYFIVE_MOVES:
         print('Draw - 75 moves without a capture or pawn move!')
      elif outcome.termination == chess.Termination.THREEFOLD_REPETITION:
         print('Draw - 3-fold repetition!')
      elif outcome.termination == chess.Termination.FIVEFOLD_REPETITION:
         print('Draw - 5-fold repetition!')
      else:
         print('Unknown outcome: ' + str(outcome))
   print(game)

# Click handler - Find which circle was clicked and what action should be taken.
def clickHandler(game, mousePos, userColor):
   global potentialMoves

   clickedSquare = getSquareFromPos(game, mousePos, userColor)

   # If the user is clicking a potential move then move there and exit
   for move in potentialMoves:
      if move.to_square == clickedSquare:
         game.push(move)
         potentialMoves = []
         return

   # If the user is clicking its own piece piece then show potential moves
   if game.color_at(clickedSquare) == userColor:
      # Reset potential moves
      potentialMoves = []

      # Find potential moves
      for move in game.legal_moves:
         if move.from_square == clickedSquare:
            potentialMoves.append(move)

   # If the user clicks elsewhere then clear potential moves
   else:
      potentialMoves = []

if __name__ == '__main__':
   main()
