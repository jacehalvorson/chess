import copy
import random
import chess

class AI:
   def __init__(self, game, color, heuristic='pieceCount'):
      self.game = game
      self.color = color

      if heuristic == 'pieceCount':
         self.heuristic = self.pieceCountHeuristic
      elif heuristic == 'random':
         self.heuristic = self.randomHeuristic
      elif heuristic == 'worstPossibleMove':
         self.heuristic = self.worstPossibleMove
      else:
         print('Unknown heuristic: ' + heuristic)
         self.heuristic = self.pieceCountHeuristic

   def minimax(self, depth):
      move, score = self.minimaxHelper(self.game, 0, depth)
      return move

   def minimaxHelper(self, game, i, depth):
      gameCopy = game.copy()

      moves = list(gameCopy.legal_moves)
      if len(moves) == 0:
         return (None, self.heuristic(gameCopy))
      
      # Initialize the best move to the first move
      best_move = moves[0]
      # Initialize the best score as -infinity when looking for maximum
      # and +infinity when looking for minimum
      best_score = float('-inf') if game.turn == self.color else float('inf')

      for moveIndex, move in enumerate(moves):
         # Make this move and check what the score is
         gameCopy.push(move)

         if i < depth:
            # Continue recursing down to find the score after <depth> moves
            _, score = self.minimaxHelper(gameCopy, i+1, depth)
         else:
            # We've reached the depth, so just get the score of the current board
            score = self.heuristic(gameCopy)

         # Check if this move is better than the best move
         isBestScore = (game.turn == self.color and score > best_score) or \
                       (game.turn != self.color and score < best_score)

         # Update the best move and score if this move is better.
         if isBestScore:
            best_move = move
            best_score = score

         # Reset the game copy to try the next move
         gameCopy = game.copy()
                     
      return (best_move, best_score)

   # Return the score of a given board based on piece counts
   def pieceCountHeuristic(self, game):
      score = 0

      # Check for checkmate
      if game.is_checkmate():
         # print(game)
         # print("Found checkmate for " + "White" if game.turn == chess.BLACK else "Black")
         if game.outcome().winner == self.color:
            return float('inf')
         else:
            return float('-inf')

      # Check for draw
      if game.can_claim_draw() or \
         game.is_stalemate() or \
         game.is_insufficient_material() or \
         game.is_seventyfive_moves() or \
         game.is_fivefold_repetition():
         return 0

      for square in chess.SQUARES:
         piece = game.piece_at(square)
         if piece is None or piece.piece_type == chess.KING:
            continue

         if piece.piece_type == chess.PAWN:
            pieceValue = 1
         elif piece.piece_type == chess.KNIGHT:
            pieceValue = 3
         elif piece.piece_type == chess.BISHOP:
            pieceValue = 3
         elif piece.piece_type == chess.ROOK:
            pieceValue = 5
         elif piece.piece_type == chess.QUEEN:
            pieceValue = 9
         else:
            print('Unknown piece type: ' + str(piece.piece_type))
            pieceValue = 0

         if piece.color == self.color:
            score += pieceValue
         else:
            score -= pieceValue

      return score

   def randomHeuristic(self, game):
      return random.randint(-100, 100)

   def worstPossibleMoveHeuristic(self, game):
      return self.pieceCountHeuristic(game) * -1
