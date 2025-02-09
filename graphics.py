import pygame
import math
import chess
from constants import *

blockArray = []
potentialMoves = []
selectedPiece = None

def initBoardGraphics():
   global blockArray

   # Set up the blockArray object, this should be called before
   # the game loop.
   for row in range(BLOCKS_IN_ROW):
      row = []
      for col in range(BLOCKS_IN_COL):
         row.append(pygame.Surface((BLOCK_SIZE, BLOCK_SIZE)))
      
      blockArray.append(row)

def getBlockCenter(row, col):
   return ((col * BLOCK_SIZE) + (BLOCK_SIZE // 2), (row * BLOCK_SIZE) + (BLOCK_SIZE // 2))

def squareToDisplayRowCol(square, userColor):
   col = chess.square_file(square)
   row = chess.square_rank(square)

   if userColor == chess.WHITE:
      return (BLOCKS_IN_ROW - 1 - row, col)
   else:
      return (row, col)

# Returns chess square of where the user clicked
def getSquareFromPos(game, mousePos, userColor):
   # Use column as is (start at 0, end at 7)
   col = int(mousePos[ 0 ] // BLOCK_SIZE)

   # If the user is white, mirror the rows so white is on bottom (start at 7, end at 0)
   if userColor == chess.WHITE:
      row = BLOCKS_IN_ROW - 1 - int(mousePos[ 1 ] // BLOCK_SIZE)
   elif userColor == chess.BLACK:
      row = int(mousePos[ 1 ] // BLOCK_SIZE)

   return chess.square(col, row)

def drawBackground(surface):
   global blockArray

   for row in range(len(blockArray)):
      # In each outer loop iteration, fill one row with blocks.
      
      for col in range(len(blockArray)):
         # Grab the block from the array
         block = blockArray[ row ][ col ]
         
         # Should this block be red or black?
         if row % 2 == col % 2:
            block.fill(BLOCK_0_COLOR)
         else:
            block.fill(BLOCK_1_COLOR)

         # Place the block on the screen
         surface.blit(block, (col * BLOCK_SIZE, row * BLOCK_SIZE))

def drawPotentialMoves(surface, userColor):
   # Draw in the potential moves
   for move in potentialMoves:
      square = move.to_square
      (row, col) = squareToDisplayRowCol(square, userColor)
      block = blockArray[ row ][ col ]

      # Inner circle
      pygame.draw.circle(block, POTENTIAL_MOVE_COLOR, (BLOCK_SIZE // 2, BLOCK_SIZE // 2), POTENTIAL_MOVE_RADIUS)
      # Outer circle for border
      pygame.draw.circle(block, POTENTIAL_MOVE_BORDER_COLOR, (BLOCK_SIZE // 2, BLOCK_SIZE // 2), POTENTIAL_MOVE_RADIUS, POTENTIAL_MOVE_BORDER_WIDTH)

      # Place the block on the screen again
      surface.blit(block, (col * BLOCK_SIZE, row * BLOCK_SIZE))

# Check which circle was clicked and what action should be taken.
# Returns list of potential moves or None
def clickHandler(game, mousePos, userColor):
   global potentialMoves

   clickedSquare = getSquareFromPos(game, mousePos, userColor)

   # If the user is clicking a potential move then move there and exit
   for move in potentialMoves:
      if move.to_square == clickedSquare:
         game.push(move)
         potentialMoves = []
         return

   # If the user is clicking a piece then show potential moves
   if game.color_at(clickedSquare) == game.turn:
      # The user clicked one of their pieces
      potentialMoves = []

      # Find potential moves
      for move in game.legal_moves:
         if move.from_square == clickedSquare:
            potentialMoves.append(move)

   # If the user clicks elsewhere then clear potential moves
   else:
      potentialMoves = []

def drawPieceInSquare(surface, pieceText, row, col):
   global blockArray

   # Find the position of the center of this block
   blockCenter = getBlockCenter(row, col)

   # Create text for piece
   font = pygame.font.Font('freesansbold.ttf', 32)
   text = font.render(pieceText, True, WHITE, None)

   # Create a rectangle to position text
   textRect = text.get_rect()
   textRect.center = blockCenter

   # Draw the text onto the block
   surface.blit(text, textRect)
