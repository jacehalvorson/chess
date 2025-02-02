from checkers.error import *
import copy

class Checkers:
   def __init__( self ):
      # Called when an instance of the class is created, do any setup needed here
      self.board = [ [0,1,0,1,0,1,0,1],
                     [1,0,1,0,1,0,1,0],
                     [0,1,0,1,0,1,0,1],
                     [0,0,0,0,0,0,0,0],
                     [0,0,0,0,0,0,0,0],
                     [2,0,2,0,2,0,2,0],
                     [0,2,0,2,0,2,0,2],
                     [2,0,2,0,2,0,2,0] ]
      self.__turn = USER_PIECE
      self.__winner = INVALID_PIECE
      return
   
   def getWinner( self ):
      return self.__winner
   
   def getTurn( self ):
      return self.__turn
   
   def __switchTurns( self ):
      self.__turn = USER_PIECE if self.__turn == AI_PIECE else AI_PIECE
      
   def __checkForWinner( self ):
      userFound = False
      aiFound = False
      
      for row in range( len( self.board ) ):
         for col in range( len( self.board[ row ] ) ):
            if self.board[ row ][ col ] in USER_TYPES:
               userFound = True
            elif self.board[ row ][ col ] in AI_TYPES:
               aiFound = True
            
            if userFound and aiFound:
               return False
            
      self.__turn = NO_PIECE
      if userFound:
         print( 'You won!' )
         self.__winner = USER_PIECE
      else:
         print( 'You lost!' )
         self.__winner = AI_PIECE
      return True
               
               
   # General move function used by the engine for a player
   # that takes in an instance of Move
   # Updates the moved piece to a king if appropriate
   def move( self, board, move, simulation ):
      if not isValidPos( move.start ) or not isValidPos( move.destination ):
         print( 'move: Invalid move from ' + str( move.start ) + ' to ' + str( move.destination ) )
         return
      
      oldRow, oldCol = move.start
      newRow, newCol = move.destination

      pieceType = board[ oldRow ][ oldCol ]
      if pieceType < 1 or pieceType > 4:
         print( 'Invalid move of pieceType ' + str( pieceType ) )
         return
      
      # Move the piece
      board[ oldRow ][ oldCol ] = 0
      board[ newRow ][ newCol ] = pieceType
      
      # Remove the jumped pieces
      for location in move.jumpedPieces:
         board[ location[0] ][ location[1] ] = 0
      
      # Check if this piece should now be a king
      if pieceType == USER_PIECE and newRow == 0:
         board[ newRow ][ newCol ] = USER_KING
      elif pieceType == AI_PIECE and newRow == 7:
         board[ newRow ][ newCol ] = AI_KING
      
      # If this is the real game board, check for a winner and switch turns
      if not simulation:
         if self.__checkForWinner( ):
            return True
         else:
            self.__switchTurns( )
            return False
      
   # Place a given piece on the board in a given location.
   # If a piece already exists at that location, replace it.
   def addPiece( self, pieceType, location ):
      if not isValidPos( location ):
         print( 'addPiece: invalid position ' + str( location ) )
         return
      if not isValidPieceType( pieceType ):
         print( 'addPiece: invalid piece type ' + str( pieceType ) )
         return
      
      row, col = location
         
      self.board[ row ][ col ] = pieceType
      
   def __getPossibleMovesHelper( self, board, pieceType, location, firstMove, ignoredDirection ):
      row, col = location
      
      if pieceType in [ USER_PIECE, USER_KING ]:
         friendlyPieceTypes = [ USER_PIECE, USER_KING ]
         opponentPieceTypes = [ AI_PIECE, AI_KING ]
      elif pieceType in [ AI_PIECE, AI_KING ]:
         friendlyPieceTypes = [ AI_PIECE, AI_KING ]
         opponentPieceTypes = [ USER_PIECE, USER_KING ]
         
      moves = []
      
      # Travel in each direction on the board looking for moves
      for direction in [ TOPLEFT, TOPRIGHT, BOTTOMLEFT, BOTTOMRIGHT ]:
         if ( ( direction == BOTTOMLEFT or direction == BOTTOMRIGHT ) and pieceType not in [ USER_KING, AI_PIECE, AI_KING ] ) or \
            ( ( direction == TOPLEFT    or direction == TOPRIGHT )    and pieceType not in [ AI_KING, USER_PIECE, USER_KING ] )   or \
            ( direction == ignoredDirection ):
            # Skip this direction
            continue

         rowChange, colChange = direction
         targetRow = row + rowChange
         targetCol = col + colChange
         targetLocation = ( targetRow, targetCol  )
         if not isValidPos( targetLocation ):
            # This target is off the board, try the next one
            continue
         
         targetPieceType = board[ targetRow ][ targetCol ]
         
         if targetPieceType in friendlyPieceTypes:
            # Friendly piece is in the way, can't move this direction
            continue

         elif targetPieceType in opponentPieceTypes:
            # Potential capture
            jumpedPiece = targetLocation
            targetLocation = ( row + 2*rowChange, col + 2*colChange )
            if not isValidPos( targetLocation ) or \
               board[ targetLocation[0] ][ targetLocation[1] ] in PIECES:
               # Invalid position or there is already a piece here, this jump won't work
               continue
            
            move = Move( location, targetLocation, [ jumpedPiece ] )
            moves.append( move )
            
            # Recursively find submoves and combine them with this one for long moves jumping multiple pieces
            for subMove in self.__getPossibleMovesHelper( board, pieceType, targetLocation, False, ( -1*rowChange, -1*colChange ) ):
               moveCopy = copy.deepcopy( move )
               moveCopy.combine( subMove )
               moves.append( moveCopy )
            
         elif firstMove:
            # Empty target, add this move with no jumped pieces to the list
            # unless we have already jumped at least once
            moves.append( Move( location, targetLocation, [] ) )
      
      return moves

   def getPossibleMoves( self, board, location ):
      row, col = location
      pieceType = board[ row ][ col ]
      
      return self.__getPossibleMovesHelper( board, pieceType, location, True, None )
      

class Move:
   def __init__( self, start, destination, jumpedPieces ):
      self.start = start
      self.destination = destination
      self.jumpedPieces = jumpedPieces
   
   def combine( self, move ):
      self.destination = move.destination
      self.jumpedPieces.extend( move.jumpedPieces )
