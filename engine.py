import math
import pygame
from checkers import *
from ai import *

blockArray = []
potentialMoves = []

def initBoard( ):
   # Set up the boardArray object, this should be called before
   # the game loop.
   for row in range( BLOCKS_IN_ROW ):
      row = []
      for col in range( BLOCKS_IN_COL ):
         row.append( pygame.Surface( ( BLOCK_SIZE, BLOCK_SIZE ) ) )
      
      blockArray.append( row )

def getBlockPosition( row, col ):
   return ( col * BLOCK_SIZE, row * BLOCK_SIZE )

def getBlockCenter( row, col ):
   ( x, y ) = getBlockPosition( row, col )
   return ( x + BLOCK_SIZE / 2, y + BLOCK_SIZE / 2 )

def getBlockFromPos( pos ):
   return ( math.floor( pos[ 1 ] / BLOCK_SIZE ), \
            math.floor( pos[ 0 ] / BLOCK_SIZE ) )

def drawBackground( surface ):   
   for row in range( len( blockArray ) ):
      # In each outer loop iteration, fill one row with blocks.
      
      for col in range( len( blockArray ) ):
         # Grab the block from the array
         block = blockArray[ row ][ col ]
         
         # Should this block be red or black?
         if row % 2 == col % 2:
            block.fill( BLOCK_0_COLOR )
         else:
            block.fill( BLOCK_1_COLOR )
         
         # Place the block on the screen
         surface.blit( block, getBlockPosition( row, col ) )
         
def placePieceInBlock( surface, piece, row, col ):
   radius = PIECE_RADIUS
   borderWidth = BORDER_WIDTH
   
   if piece == USER_PIECE:
      color = USER_PIECE_COLOR
      borderColor = USER_BORDER_COLOR
   elif piece == USER_KING:
      color = USER_KING_COLOR
      borderColor = USER_BORDER_COLOR
   elif piece == AI_PIECE:
      color = AI_PIECE_COLOR
      borderColor = AI_BORDER_COLOR
   elif piece == AI_KING:
      color = AI_KING_COLOR
      borderColor = AI_BORDER_COLOR
   elif piece == POTENTIAL_MOVE:
      color = POTENTIAL_MOVE_COLOR
      borderColor = POTENTIAL_MOVE_BORDER_COLOR
      radius = POTENTIAL_MOVE_RADIUS
      borderWidth = POTENTIAL_MOVE_BORDER_WIDTH
   elif piece == NO_PIECE:
      return
   else:
      print( 'placePieceInBlock: Invalid piece type ' + str( piece ) )
      return
      
   # Grab the block we're drawing this circle onto
   block = blockArray[ row ][ col ]
   
   # Find the center of the block
   blockCenter = ( BLOCK_SIZE / 2, BLOCK_SIZE / 2 )
   
   # Draw the circle onto the block
   pygame.draw.circle( block, color, blockCenter, radius )
   pygame.draw.circle( block, borderColor, blockCenter, radius, borderWidth )
   surface.blit( block, getBlockPosition( row, col ) )   

# Returns row and col of circle that is being clicked. If the click is
# not within a circle, (-1, -1) is returned
def getCircleFromPos( game, mousePos ):
   # Check if there is a piece where the mouse click was
   # within PIECE_RADIUS pixels of the center of the circle
   ( row, col ) = getBlockFromPos( mousePos )
   ( x, y ) = getBlockCenter( row, col )
   
   # Calculate the manhattan distance from the center of this block
   sqx = ( mousePos[ 0 ] - x ) ** 2
   sqy = ( mousePos[ 1 ] - y ) ** 2
   if math.sqrt( sqx + sqy ) < PIECE_RADIUS and game.board[ row ][ col ] != 0:
      # The click is within the circle size and there is
      # a piece in this block, return its board index
      return ( row, col )
   return ( -1, -1 )

def clearPotentialMoves( game ):
   global potentialMoves

   # Clear any potential move icons
   for move in potentialMoves:
      game.addPiece( 0, move.destination )
   
   # Empty the temporary list
   potentialMoves = []
            
# Check which circle was clicked and what action should be taken.
# Returns list of potential moves
def clickHandler( game, mousePos ):
   global potentialMoves
   
   # Check if a piece was clicked
   ( row, col ) = getCircleFromPos( game, mousePos )
   if row == -1 or col == -1:
      clearPotentialMoves( game )
      return
   pieceType = game.board[ row ][ col ]
   
   # If the user is clicking a potential move then move there
   if pieceType == POTENTIAL_MOVE:
      # Find the move with this destination
      move = None
      for potentialMove in potentialMoves:
         if potentialMove.destination == ( row, col ):
            move = potentialMove
            break
      if move == None:
         print( f'clickHandler: move to {( row, col )} not found' )
         return
      
      game.move( game.board, move, False )
      
      potentialMoves.remove( move )
      clearPotentialMoves( game )
   
   elif pieceType == USER_PIECE or pieceType == USER_KING:
      # The user clicked one of their pieces
      clearPotentialMoves( game )
         
      # Find potential moves
      if pieceType == USER_PIECE or pieceType == USER_KING:
         moves = game.getPossibleMoves( game.board, ( row, col ) )
         
         # Add icons to the board for potential moves
         for move in moves:
            game.addPiece( POTENTIAL_MOVE, move.destination )
            potentialMoves.append( move )


def main( ):
   # Initialize pygame
   pygame.init( )
   
   # Create objects for each block on the board
   initBoard( )
   
   # Set up checkers game
   game = Checkers( )
   # game.board = [ [0,0,0,1,0,0,0,0],
   #                [0,0,1,0,0,0,0,0],
   #                [0,0,0,0,0,0,0,0],
   #                [0,0,0,0,1,0,0,0],
   #                [0,0,0,0,0,2,0,0],
   #                [2,0,0,0,2,0,2,0],
   #                [0,2,0,2,0,2,0,2],
   #                [2,0,2,0,2,0,2,0] ]
   
   # Initialize AI
   AI = checkersAI( game )

   # Set up game window
   screen = pygame.display.set_mode( [ WINDOW_WIDTH, WINDOW_HEIGHT ] )
   pygame.display.set_caption( 'Checkers' )

   # Initialize clock
   clock = pygame.time.Clock( )

   # Loop until the window is closed by the user
   numIterations = 0
   loop = True
   while loop:
      # Check for input
      for event in pygame.event.get( ):
         
         if event.type == pygame.MOUSEBUTTONDOWN:
            if game.getTurn( ) == USER_PIECE:
               clickHandler( game, pygame.mouse.get_pos( ) )

         elif event.type == pygame.QUIT:
            loop = False
      
      # Get checkered background
      drawBackground( screen )
      
      # Draw in pieces found in the board array
      for rowIndex, rowArray in enumerate( game.board ):
         for colIndex, piece in enumerate( rowArray ):
            placePieceInBlock( screen, piece, rowIndex, colIndex )
      
      # Update the screen
      pygame.display.update( )

      if game.getTurn( ) == AI_PIECE:
         bestMove = AI.minMax( game.board, 0, 3 )[ 1 ]
         game.move( game.board, bestMove, False )
               
      # Ensure the game doesn't run faster than CLOCK_RATE fps
      clock.tick( CLOCK_RATE )
      numIterations += 1
   # end while Loop
   
   # Opposite of pygame.init( )
   pygame.quit()

if __name__ == '__main__':
   main()
