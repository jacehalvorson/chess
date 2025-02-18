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

      legalMoves = list(game.legal_moves)

      # Iterative deepening
      for i in range(1, depth + 1):
         print(f'Depth {i}')
         move, score, allScores = self.minimaxHelper(game, legalMoves, depth, float('-inf'), float('inf'))
         legalMoves.sort(key=lambda move: allScores[move], reverse=True)
         if len(legalMoves) > 4:
            print(f'Top 5 moves: {legalMoves[0]} {legalMoves[1]} {legalMoves[2]} {legalMoves[3]} {legalMoves[4]}')

      print(f'{nodesConsidered} Nodes considered in {timeit.default_timer() - start} seconds with depth {depth}')
      return move

   def minimaxHelper(self, game, moves, depth, alpha, beta):
      global nodesConsidered

      # Dictionary to map moves to their scores
      moveScores = {}

      if depth == 0 or game.is_game_over():
         return (None, self.heuristic(game), moveScores)

      # Determine if this is a MIN level or MAX level
      maximizing = game.turn == self.color

      # Initialize the best move to the first move
      bestMoves = [moves[0]]

      if maximizing:
         bestScore = float('-inf')
         for moveIndex, move in enumerate(moves):
            # Make the move
            game.push(move)
            nodesConsidered += 1

            # Recursively call minimax
            _, score, _ = self.minimaxHelper(game, list(game.legal_moves), depth - 1, alpha, beta)
            moveScores[move] = score
            
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

         return (random.choice(bestMoves), bestScore, moveScores)
      else:
         bestScore = float('inf')
         for moveIndex, move in enumerate(moves):
            # Make the move
            game.push(move)
            nodesConsidered += 1
            
            # Recursively call minimax
            _, score, _ = self.minimaxHelper(game, list(game.legal_moves), depth - 1, alpha, beta)
            moveScores[move] = score

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

         return (random.choice(bestMoves), bestScore, moveScores)

         # Reset the game copy to try the next move
         game.pop()

      return (random.choice(bestMoves), bestScore, moveScores)

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
