import copy
import random

class AI:
   def __init__(self, game, color):
      self.game = game
      self.color = color
   
   # Return the heuristic value for a player within a given game.
   def getScore(self, game):
      return random.random()

   def minimax(self, depth):
      move, score = self.minimaxHelper(self.game, 0, depth)
      return move

   def minimaxHelper(self, game, i, depth):
      gameCopy = game.copy()

      moves = list(gameCopy.legal_moves)
      if len(moves) == 0:
         return (None, self.getScore(gameCopy))
      
      # Initialize the best move to the first move
      best_move = moves[0]
      # Initialize the best score as -infinity when looking for maximum,
      # or infinity when looking for minimum
      best_score = float('-inf') if gameCopy.turn == self.color else float('inf')

      for move in moves:
         # Make this move and check what the score is
         gameCopy.push(move)

         if i < depth:
            # Continue recursing down to find the score after <depth> moves
            _, score = self.minimaxHelper(gameCopy, i+1, depth)
         else:
            # We've reached the depth, so just get the score of the current board
            score = self.getScore(gameCopy)

         # A "better" move is one that has a higher score if it's the AI's turn
         # or a lower score if it's the player's turn.
         isBestScore = (score > best_score) if game.turn == self.color else (score < best_score)

         # Update the best move and score if this move is better.
         if isBestScore:
            best_move = move
            best_score = score

         # Reset the game copy to try the next move
         gameCopy = game.copy()
                     
      return (best_move, best_score)
