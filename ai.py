import copy
import random
import chess
import timeit

PIECE_VALUES = {
   chess.PAWN: 1,
   chess.KNIGHT: 3,
   chess.BISHOP: 3,
   chess.ROOK: 5,
   chess.QUEEN: 9,
   chess.KING: 0
}

nodesConsidered = 0
verbose = 1
heuristicTime = 0
heuristicCount = 0
      
class chessAI:
   def __init__(self, color, heuristic='position'):
      self.color = color

      if heuristic == 'position':
         self.heuristic = self.positionHeuristic
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

      # Iterative deepening - Start with depth 1 and sort by score, then increase depth
      # sorting at each step. This allows for efficient pruning
      for i in range(1, depth + 1):
         moveSequence, score, allScores = self.minimaxHelper(game, legalMoves, i, float('-inf'), float('inf'))
         legalMoves.sort(key=lambda move: allScores[move], reverse=True)

      if verbose >= 2:
         print('Planning on', end=' ')
         for move in moveSequence:
            print(str(move), end=' ')
         print()
         for move in legalMoves:
            print(f'{move} {allScores[move]}', end=' ')
         print()

      if verbose >= 1:
         print(f'{nodesConsidered} Nodes considered in {timeit.default_timer() - start} seconds with depth {depth}')
         print(f'Average heuristic time: {heuristicTime / heuristicCount * 1000000} µs')

      return moveSequence[0]

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
         for move in moves:
            # Make the move
            game.push(move)
            nodesConsidered += 1

            # Recursively call minimax
            nextMove, score, _ = self.minimaxHelper(game, list(game.legal_moves), depth - 1, alpha, beta)
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

      else:
         bestScore = float('inf')
         for move in moves:
            # Make the move
            game.push(move)
            nodesConsidered += 1
            
            # Recursively call minimax
            nextMove, score, _ = self.minimaxHelper(game, list(game.legal_moves), depth - 1, alpha, beta)
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

      moveSequence = [random.choice(bestMoves)]
      if nextMove is not None:
         moveSequence.extend(nextMove)

      return (moveSequence, bestScore, moveScores)

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
      global heuristicTime
      global heuristicCount
      
      CHECK_BIAS = 5
      PIECE_WEIGHT = 15
      ATTACKER_WEIGHT = 3
      SUPPORTER_WEIGHT = 1
      VISIBLE_WEIGHT = 1

      score = 0

      start = timeit.default_timer()
      
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

      if game.is_check():
         if game.turn == self.color:
            score -= CHECK_BIAS
         else:
            score += CHECK_BIAS

      # For each piece
      for square, piece in game.piece_map(mask=(game.occupied_co[self.color])).items():
         # Piece count
         # Take away points for every attacker on this piece
         # Add points for every piece that's supporting this one
         # Add points for every square that this piece can see
         score += \
            PIECE_WEIGHT * PIECE_VALUES[piece.piece_type] - \
            ATTACKER_WEIGHT * PIECE_VALUES[piece.piece_type] * len(game.attackers(not self.color, square)) + \
            SUPPORTER_WEIGHT * PIECE_VALUES[piece.piece_type] * len(game.attackers(self.color, square)) + \
            VISIBLE_WEIGHT * len(game.attacks(square))

      for square, piece in game.piece_map(mask=(game.occupied_co[not self.color])).items():
         # Piece count
         # Take away points for every attacker on this piece
         # Add points for every piece that's supporting this one
         # Add points for every square that this piece can see
         score -= \
            PIECE_WEIGHT * PIECE_VALUES[piece.piece_type] - \
            ATTACKER_WEIGHT * PIECE_VALUES[piece.piece_type] * len(game.attackers(self.color, square)) + \
            SUPPORTER_WEIGHT * PIECE_VALUES[piece.piece_type] * len(game.attackers(not self.color, square)) + \
            VISIBLE_WEIGHT * len(game.attacks(square))

      heuristicTime += timeit.default_timer() - start
      heuristicCount += 1

      return score

   def randomHeuristic(self, game):
      return random.randint(-100, 100)

   def worstPossibleMoveHeuristic(self, game):
      return self.positionHeuristic(game) * -1
