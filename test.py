import chess
import chess.pgn
from ai import chessAI

def main():
   ai = chessAI(chess.WHITE)
   with open('game.pgn') as pgn:
      # Load the first game from the PGN file
      game = chess.pgn.read_game(pgn)
      
      if game is None:
         print("No game found in the PGN file")
         return 1

   # Convert game moves to a list
   moves = list(game.mainline_moves())

   # If some indexes exceed the game length
   max_index = len(moves) - 1
   for index in [3, 17, 25, 31, 43]:
      if index > max_index:
         print(f"Move {index}: Not available (game has only {max_index + 1} moves)")
         return 1
   
   situations = []
   game = game.board()  # Starting position
   
   for i, move in enumerate(moves):
      if i in [3, 17, 25, 31, 43]:
         situations.append(game.copy())
      
      # Next move
      game.push(move)

   for situation in situations:
      print("AI move:", ai.minimax(situation, depth=3))
      print()

   return 0

if __name__ == "__main__":
   main()
