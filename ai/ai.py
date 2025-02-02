from checkers import *
import copy

class checkersAI:
   def __init__( self, game ):
      self.game = game
      self.board = game.board
   
   # Return the heuristic value for a player on a given board.
   # Player is USER_PIECE or AI_PIECE
   def getScore( self, board, player ):
      pieceCounts = { USER_PIECE:0, AI_PIECE:0 }
      kingCounts = { USER_PIECE:0, AI_PIECE:0 }
      immortalCounts = { USER_PIECE:0, AI_PIECE:0 }
      countIndex = INVALID_PIECE
      
      for row in range( len( board ) ):
         for col in range( len ( board[ row ] ) ):
            pieceType = board[ row ][ col ]
            
            if pieceType in USER_TYPES:
               countIndex = USER_PIECE
            elif pieceType in AI_TYPES:
               countIndex = AI_PIECE
            else:
               # Empty block or potential move, skip this one
               continue

            if col == 0 or col == 7 or row == 0 or row == 7:
               # This piece is untakable
               immortalCounts[ countIndex ] += 1
            
            if pieceType in PAWN_PIECES:
               pieceCounts[ countIndex ] += 1
            elif pieceType in KING_PIECES:
               kingCounts[ countIndex ] += 1
      
      # Calculate score
      score = ( pieceCounts[ AI_PIECE ] + 2*kingCounts[ AI_PIECE ] + 0.2*immortalCounts[ AI_PIECE ] ) \
            - ( pieceCounts[ USER_PIECE ] + 2*kingCounts[ USER_PIECE ] + 0.2*immortalCounts[ USER_PIECE ] )
            
      if pieceCounts[ AI_PIECE ] + kingCounts[ AI_PIECE ] == 0:
         score = float( '-inf' )
      if pieceCounts[ USER_PIECE ] + kingCounts[ USER_PIECE ] == 0:
         score = float( 'inf' )
         
      return( score )
   
   
   def minMax( self, board, i, depth ):
      boardCopy = copy.deepcopy(board)
      
      if i % 2 == 0:
         player = AI_PIECE
      if i % 2 == 1:
         player = USER_PIECE
      
      moves = self.getAllPossibleMoves( player,boardCopy )
      if moves == []:
         return ( self.getScore( boardCopy, player ), None )
         
      best_move = moves[0]
      if player == AI_PIECE:
         best_score = float( '-inf' )
      else:
         best_score = float( 'inf' )

      for move in moves:
         self.game.move( boardCopy, move, True )
         if i < depth:
            score = self.minMax( boardCopy, i+1, depth )[0]
         else:
            score = self.getScore( boardCopy, player )  
      
         if player == AI_PIECE:
            isBestScore = ( score > best_score )
         else:
            isBestScore = ( score < best_score )

         if isBestScore:
            best_score = score
            best_move = move
      
         # Reset the board copy
         boardCopy = copy.deepcopy( board )
                     
      return( best_score, best_move )
   
   
   def getAllPossibleMoves( self, pieceType, board ):
      moves = []
      
      for row in range( len( board ) ):
         for col in range( len ( board[ row ] ) ):
            
            if pieceType in [ USER_PIECE, USER_KING ] and \
               board[ row ][ col ] in [ USER_PIECE, USER_KING ]:
                  
               moves.extend( self.game.getPossibleMoves( board, ( row, col ) ) )
               
            elif pieceType in [ AI_PIECE, AI_KING ] and \
               board[ row ][ col ] in [ AI_PIECE, AI_KING ]:
                  
               moves.extend( self.game.getPossibleMoves( board, ( row, col ) ) )
      
      return moves
