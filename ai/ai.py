import copy
import random
import chess

movesConsidered = 0

class chessAI:
   def __init__(self, color, heuristic='pieceCount'):
      self.color = color

      if heuristic == 'pieceCount':
         self.heuristic = self.pieceCountHeuristic
      elif heuristic == 'random':
         self.heuristic = self.randomHeuristic
      elif heuristic == 'worstPossibleMove':
         self.heuristic = self.worstPossibleMoveHeuristic
      else:
         print('Unknown heuristic: ' + heuristic)
         self.heuristic = self.pieceCountHeuristic

   def minimax(self, game, depth):
      global movesConsidered
      movesConsidered = 0
      move, score = self.minimaxHelper(game, depth, float('-inf'), float('inf'))
      print('Moves considered: ' + str(movesConsidered))
      return move

   def minimaxHelper(self, game, depth, alpha, beta):
      global movesConsidered

      # Determine if this is a MIN level or MAX level
      maximizing = game.turn == self.color
      
      # Get all legal moves
      moves = list(game.legal_moves)
      if depth == 0 or len(moves) == 0:
         return (None, self.heuristic(game))

      # Initialize the best move to the first move
      bestMoves = [moves[0]]
      # Initialize the best score as -infinity when looking for maximum
      # and +infinity when looking for minimum
      bestScore = float('-inf') if maximizing else float('inf')

      for move in moves:
         # Make this move and check what the score is
         game.push(move)
         movesConsidered += 1

         # Continue recursing down to find the score after <depth> moves
         _, score = self.minimaxHelper(game, depth - 1, alpha, beta)

         # Check if this move is better than the best move
         isBestScore = (maximizing and score > bestScore) or \
                       (not maximizing and score < bestScore)

         # Update the best move and score if this move is better.
         if isBestScore:
            bestMoves = [move]
            bestScore = score
         # If it ties, randomly choose between the two.
         elif score == bestScore:
            bestMoves.append(move)

         # Reset the game copy to try the next move
         game.pop()

      return (random.choice(bestMoves), bestScore)

   # Return the score of a given board based on piece counts
   def pieceCountHeuristic(self, game):
      PIECE_VALUES = {
         chess.PAWN: 1,
         chess.KNIGHT: 3,
         chess.BISHOP: 3,
         chess.ROOK: 5,
         chess.QUEEN: 9
      }

      score = 0

      # Only check for checkmate/draw if the game is over to save time
      if game.is_game_over():
         # Check for checkmate
         if game.is_checkmate():
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

      for piece in game.piece_map().values():
         if piece.piece_type == chess.KING:
            continue

         pieceValue = PIECE_VALUES[piece.piece_type]

         if piece.color == self.color:
            score += pieceValue
         else:
            score -= pieceValue

      return score

   def randomHeuristic(self, game):
      return random.randint(-100, 100)

   def worstPossibleMoveHeuristic(self, game):
      return self.pieceCountHeuristic(game) * -1
