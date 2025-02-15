import pygame
import math
import chess
import chess.svg
import io

blockArray = []
selectedPiece = None

# Constants for board graphics
WINDOW_WIDTH = 600
WINDOW_HEIGHT = 600
BLOCKS_IN_ROW = 8
BLOCKS_IN_COL = BLOCKS_IN_ROW
NUM_BLOCKS = BLOCKS_IN_ROW * BLOCKS_IN_ROW
BLOCK_SIZE = ( WINDOW_WIDTH / BLOCKS_IN_ROW )
BLOCK_0_COLOR = '#52311e'
BLOCK_1_COLOR = '#c59562'

# Potential move circle
POTENTIAL_MOVE = 5
POTENTIAL_MOVE_COLOR = (0, 255, 255)
POTENTIAL_MOVE_RADIUS = BLOCK_SIZE * (1/8)
POTENTIAL_MOVE_BORDER_COLOR = (255, 255, 255)
POTENTIAL_MOVE_BORDER_WIDTH = 1

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

def drawPotentialMoves(surface, potentialMoves, userColor):
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

def drawPieceInSquare(surface, piece, row, col):
   global blockArray

   # Find the position of the center of this block
   blockCenter = getBlockCenter(row, col)

   # Create text for piece
   image = str(chess.svg.piece(piece))
   imageSurface = pygame.image.load(io.BytesIO(image.encode()))

   # Create a rectangle to position text
   rect = imageSurface.get_rect()
   rect.center = blockCenter

   # Draw the text onto the block
   surface.blit(imageSurface, rect)
