import pygame
import chess
from constants import *
from graphics import *
from ai import *

def main():
   # Initialize pygame
   pygame.init()
   
   # Create objects for each block on the board
   initBoard()
   
   # Set up checkers game
   game = chess.Board()
   userColor = chess.WHITE

   # Initialize AI
   # AI = checkersAI(game)

   # Set up game window
   screen = pygame.display.set_mode([ WINDOW_WIDTH, WINDOW_HEIGHT ])
   pygame.display.set_caption('Chess')

   # Initialize clock
   clock = pygame.time.Clock()

   # Loop until the window is closed by the user
   numIterations = 0
   loop = True
   while loop:
      # Check for input
      for event in pygame.event.get():
         if event.type == pygame.MOUSEBUTTONDOWN and game.turn == userColor:
            clickHandler(game, pygame.mouse.get_pos(), userColor)
         elif event.type == pygame.QUIT:
            loop = False
      
      # Draw checkered background
      drawBackground(screen)
      
      # Draw in pieces found on the board
      for square in chess.SQUARES:
         piece = game.piece_at(square)
         if piece != None:
            # Use column as is (start at 0, end at 7)
            col = chess.square_file(square)

            # If the user is white, mirror the rows so white is on bottom (start at 7, end at 0)
            if userColor == chess.WHITE:
               row = BLOCKS_IN_ROW - 1 - chess.square_rank(square)
            elif userColor == chess.BLACK:
               row = chess.square_rank(square)

            drawPieceInSquare(screen, piece.symbol(), row, col)
      
      # Update the screen
      pygame.display.update()

      # if game.getTurn() == AI_PIECE:
      #    bestMove = AI.minMax(game.board, 0, 3)[ 1 ]
      #    game.move(game.board, bestMove, False)
               
      # Ensure the game doesn't run faster than CLOCK_RATE fps
      clock.tick(CLOCK_RATE)
      numIterations += 1
   
   # Opposite of pygame.init()
   pygame.quit()

if __name__ == '__main__':
   main()
