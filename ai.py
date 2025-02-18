import copy
import random
import chess
import timeit

PIECE_VALUES = {
   chess.PAWN: 1,
   chess.KNIGHT: 3,
   chess.BISHOP: 3,
   chess.ROOK: 5,
   chess.QUEEN: 9
}

nodesConsidered = 0

class chessAI:
   def __init__(self, color, heuristic='pieceCount'):
      self.color = color

      if heuristic == 'position':
         self.heuristic = self.pieceCountHeuristic
      elif heuristic == 'pieceCount':
         self.heuristic = self.pieceCountHeuristic
      elif heuristic == 'random':
         self.heuristic = self.randomHeuristic
      elif heuristic == 'worst':
         self.heuristic = self.worstPossibleMoveHeuristic
      else:
         print('Unknown heuristic: ' + heuristic)
         self.heuristic = self.pieceCountHeuristic

   def minimax(self, game, depth):
      global nodesConsidered
      nodesConsidered = 0
      start = timeit.default_timer()
      
      move, score = self.minimaxHelper(game, depth, float('-inf'), float('inf'))

      print(f'{nodesConsidered} Nodes considered in {timeit.default_timer() - start} seconds with depth {depth}')
      return move

   def minimaxHelper(self, game, depth, alpha, beta):
      global nodesConsidered

      # Determine if this is a MIN level or MAX level
      maximizing = game.turn == self.color
      
      # Get all legal moves
      moves = list(game.legal_moves)
      if depth == 0 or len(moves) == 0:
         return (None, self.heuristic(game))

      # Sort the moves by likelihood of being good
      def moveSortFunction(move):
         if game.gives_check(move):
            return 2
         elif game.is_capture(move):
            return 1
         return 0

      moves.sort(key=lambda move: moveSortFunction(move), reverse=maximizing)

      # Initialize the best move to the first move
      bestMoves = [moves[0]]

      if maximizing:
         bestScore = float('-inf')
         for moveIndex, move in enumerate(moves):
            # Make the move
            game.push(move)
            nodesConsidered += 1

            # Recursively call minimax
            _, score = self.minimaxHelper(game, depth - 1, alpha, beta)
            
            # Reset the board
            game.pop()

            # Evaluate best scores
            if score > bestScore:
               bestMoves = [move]
               bestScore = score
               alpha = max(alpha, bestScore)
            elif score == bestScore:
               bestMoves.append(move)

            # Alpha beta pruning
            if bestScore > beta:
               break

         return (random.choice(bestMoves), bestScore)
      else:
         bestScore = float('inf')
         for moveIndex, move in enumerate(moves):
            # Make the move
            game.push(move)
            nodesConsidered += 1
            
            # Recursively call minimax
            _, score = self.minimaxHelper(game, depth - 1, alpha, beta)

            # Reset the board
            game.pop()

            # Evaluate best scores
            if score < bestScore:
               bestMoves = [move]
               bestScore = score
               beta = min(beta, bestScore)
            elif score == bestScore:
               bestMoves.append(move)

            # Alpha beta pruning
            if bestScore < alpha:
               break

         return (random.choice(bestMoves), bestScore)

         # Reset the game copy to try the next move
         game.pop()

      return (random.choice(bestMoves), bestScore)

   # Return the score of a given board based on piece counts
   def pieceCountHeuristic(self, game):
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

   # Start with pieceCount and include attackers, checks, and visible squares
   def positionHeuristic(self, game):
      CHECK_BIAS = 5
      ATTACKER_WEIGHT = 4
      SUPPORTER_WEIGHT = 1
      VISIBLE_WEIGHT = 2

      score = pieceCountHeuristic(game) * 10
      
      if game.is_check():
         # Take away points if currently in check
         if game.turn == self.color:
            score -= CHECK_BIAS
         else:
            score += CHECK_BIAS

      # For each piece of the AI's
      for piece in game.piece_map().values():
         if piece.color is not self.color:
            continue

         # Take away points for every attacker on this piece
         score -= ATTACKER_WEIGHT * PIECE_VALUES[piece.piece_type] * len(game.attackers(not self.color, piece.square))

         # Add points for every piece that's supporting this one
         score += SUPPORTER_WEIGHT * PIECE_VALUES[piece.piece_type] * len(game.attackers(self.color, piece.square))

         # Add points for every square that this piece can see
         for square in game.attacks(piece.square):
            score += VISIBLE_WEIGHT
      
      return score

   def randomHeuristic(self, game):
      return random.randint(-100, 100)

   def worstPossibleMoveHeuristic(self, game):
      return self.positionHeuristic(game) * -1
