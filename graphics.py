import pygame
import math
import chess
from constants import *

blockArray = []
potentialMoves = []
selectedPiece = None

def initBoard():
   global blockArray

   # Set up the blockArray object, this should be called before
   # the game loop.
   for row in range(BLOCKS_IN_ROW):
      row = []
      for col in range(BLOCKS_IN_COL):
         row.append(pygame.Surface((BLOCK_SIZE, BLOCK_SIZE)))
      
      blockArray.append(row)

def clearPotentialMoves(game):
   global potentialMoves

   # Clear any potential move icons
   for move in potentialMoves:
      game.addPiece(0, move.destination)
   
   # Empty the temporary list
   potentialMoves = []

def getBlockPosition(row, col):
   return (col * BLOCK_SIZE, row * BLOCK_SIZE)

def getBlockCenter(row, col):
   return ((col * BLOCK_SIZE) + (BLOCK_SIZE / 2), (row * BLOCK_SIZE) + (BLOCK_SIZE / 2))

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
         surface.blit(block, getBlockPosition(row, col))

# Returns chess square of where the user clicked
def getSquareFromPos(game, mousePos):
   row = math.floor(mousePos[ 1 ] / BLOCK_SIZE)
   col = math.floor(mousePos[ 0 ] / BLOCK_SIZE)

   return chess.square(row, col)

# Check which circle was clicked and what action should be taken.
# Returns list of potential moves or None
def clickHandler(game, mousePos, userColor):
   global potentialMoves

   clickedSquare = getSquareFromPos(game, mousePos)

   # If the user is clicking a potential move then move there
   if clickedSquare in potentialMoves:
      # Find the move with this destination
      # TODO move selectedPiece to clickedSquare
      clearPotentialMoves(game)

   elif game.color_at(clickedSquare) == userColor:
      # The user clicked one of their pieces
      clearPotentialMoves(game)

      # Find potential moves
      for move in game.legal_moves:
         if move.from_square == clickedSquare:
            potentialMoves.append(move.to_square)

def drawPieceInSquare(surface, pieceText, row, col):
   global blockArray

   # Find the center of the block we're drawing this piece onto
   block = blockArray[ row ][ col ]

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
