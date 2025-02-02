from checkers.constants import *

def isValidPieceType( pieceType ):
   if pieceType == USER_PIECE:
      return True
   elif pieceType == USER_KING:
      return True
   elif pieceType == AI_PIECE:
      return True
   elif pieceType == AI_KING:
      return True
   elif pieceType == POTENTIAL_MOVE:
      return True
   elif pieceType == NO_PIECE:
      return True
   else:
      return False

def isValidPos( pos ):
   row, col = pos
   
   if row < 0 or row >= BLOCKS_IN_ROW or col < 0 or col >= BLOCKS_IN_COL:
      return False

   return True
