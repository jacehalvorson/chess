from pathlib import Path
import os
# Hide the pygame support prompt (must be before pygame import)
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = '1'
import argparse
import pygame
import chess
import chess.engine

from graphics import *
from ai import chessAI

CLOCK_RATE = 60
DEPTH = 3

# Holds blue dots that show potential moves from the user's selected piece
potentialMoves = []

def main():
   parser = argparse.ArgumentParser(prog='python3 engine.py', description='Play chess against an AI or watch 2 AIs play against each other')
   parser.add_argument('--stockfish', '-s', action='store_true', help='Instead of playing against the AI, watch it go up against Stockfish')
   parser.add_argument('--color', '-c', default='white', help='Choose the color on the bottom of the screen (white or black)')
   parser.add_argument('--heuristic', default='position', help="Choose the AI's method of evaluating the board state. Options: position, pieceCount, random, worst")
   args = parser.parse_args()
   
   if args.color.lower() not in ['white', 'black']:
      parser.print_help()
      print('')
      print('Invalid color argument. Must be either white or black')
      return 1
   if args.heuristic.lower() not in ['piececount', 'position', 'random', 'worst']:
      parser.print_help()
      print('')
      print('Invalid heuristic argument. Must be either pieceCount, position, random, or worst')
      return 1

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
   if args.stockfish:
      # Check if Stockfish is in the current directory
      if not os.path.isfile('stockfish.exe'):
         print()
         print("Cannot find Stockfish executable. Download from https://stockfishchess.org/download/ "
               "and copy the *.exe file into this repository, renaming it to 'stockfish.exe'")
         return 1

      # Create the AIs
      ai = chessAI(userColor, heuristic=args.heuristic)
      stockfish = chess.engine.SimpleEngine.popen_uci('stockfish.exe')
      stockfish.configure({"UCI_elo": 1320, "UCI_LimitStrength": "true"})
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

      # If playing against Stockfish, then play the best move from the current turn
      if args.stockfish:
         if game.turn == userColor:
            bestMove = ai.minimax(game, depth=DEPTH)
            game.push(bestMove)
         elif game.turn == aiColor:
            result = stockfish.play(game, chess.engine.Limit(time=0.1), ponder=False)
            game.push(result.move)
      # If the user is playing then play the bext move from the AI
      else:
         if game.turn == aiColor:
            bestMove = ai.minimax(game, depth=DEPTH)
            game.push(bestMove)

      # Ensure the game doesn't run faster than CLOCK_RATE fps
      clock.tick(CLOCK_RATE)
      numIterations += 1
   
   # Opposite of pygame.init()
   pygame.quit()

   if args.stockfish:
      stockfish.quit()

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
   
   return 0

if __name__ == '__main__':
   main()
