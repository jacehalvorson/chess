import pygame
import chess
from constants import *
from graphics import *
from ai import *

# Holds blue dots that show potential moves from the user's selected piece
potentialMoves = []

def main():
   # Initialize pygame
   pygame.init()
   
   # Create objects for each block on the board
   initBoardGraphics()
   
   # Set up checkers game
   game = chess.Board()
   
   # Define colors
   userColor = chess.WHITE
   aiColor = chess.BLACK if userColor == chess.WHITE else chess.WHITE

   # Initialize AI
   ai = AI(game, aiColor)

   # Set up game window
   screen = pygame.display.set_mode([ WINDOW_WIDTH, WINDOW_HEIGHT ])
   pygame.display.set_caption('Chess')

   # Initialize clock
   clock = pygame.time.Clock()

   # Loop until the window is closed by the user
   numIterations = 0
   loop = True
   while loop and not game.is_game_over():
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
            drawPieceInSquare(screen, piece.symbol(), row, col)

      # Draw in the potential moves
      drawPotentialMoves(screen, potentialMoves, userColor)

      # Update the screen
      pygame.display.update()

      # AI's turn
      if game.turn == aiColor:
         bestMove = ai.minimax(depth=1)
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
   if game.outcome():
      print(game.outcome().termination)
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
