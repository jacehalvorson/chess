import copy
import random
import chess

movesConsidered = 0
movesSkipped = 0

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
      global movesSkipped
      movesConsidered = 0
      movesSkipped = 0
      move, score = self.minimaxHelper(game, depth, float('-inf'), float('inf'))
      print('Moves considered: ' + str(movesConsidered))
      print('Moves skipped: ' + str(movesSkipped))
      return move

   def minimaxHelper(self, game, depth, alpha, beta):
      global movesConsidered
      global movesSkipped

      # Determine if this is a MIN level or MAX level
      maximizing = game.turn == self.color
      
      # Get all legal moves
      moves = list(game.legal_moves)
      if depth == 0 or len(moves) == 0:
         return (None, self.heuristic(game))

      # Initialize the best move to the first move
      bestMoves = [moves[0]]

      if maximizing:
         bestScore = float('-inf')
         for moveIndex, move in enumerate(moves):
            # Make the move
            game.push(move)
            movesConsidered += 1

            # Recursively call minimax
            _, score = self.minimaxHelper(game, depth - 1, alpha, beta)
            
            # Reset the board
            game.pop()

            # Evaluate best scores
            if score > bestScore:
               bestMoves = [move]
               bestScore = score
            elif score == bestScore:
               bestMoves.append(move)

            # Alpha beta pruning
            alpha = max(alpha, bestScore)
            if bestScore >= beta:
               movesSkipped = len(moves) - moveIndex - 1
               break

         return (random.choice(bestMoves), bestScore)
      else:
         bestScore = float('inf')
         for moveIndex, move in enumerate(moves):
            # Make the move
            game.push(move)
            movesConsidered += 1
            
            # Recursively call minimax
            _, score = self.minimaxHelper(game, depth - 1, alpha, beta)

            # Reset the board
            game.pop()

            # Evaluate best scores
            if score < bestScore:
               bestMoves = [move]
               bestScore = score
            elif score == bestScore:
               bestMoves.append(move)

            # Alpha beta pruning
            beta = min(beta, bestScore)
            if bestScore <= alpha:
               movesSkipped = len(moves) - moveIndex - 1
               break

         return (random.choice(bestMoves), bestScore)

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
