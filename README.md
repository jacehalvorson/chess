# Chess Engine

- [Chess Engine](#chess-engine)
  - [How to Run](#how-to-run)
    - [Windows](#windows)
    - [Linux](#linux)
  - [Heuristic options](#heuristic-options)

Play Chess against a minimax algorithm.

> Note: Originally imported from Checkers repository https://github.com/gpatt45/checkers_bot

## How to Run

### Windows

If you don't have Python installed, run this to open it in the Microsoft Store and install it.

```bash
python3
```

If you don't have pip installed, run this to install it.

```bash
python3 -m ensurepip --upgrade
```

Install dependencies for this app.

```bash
python3 -m pip install python-chess pygame
```

Run the app.

```bash
python3 engine.py
```

### Linux

If you don't have Python and pip installed, run this to install them.

```bash
sudo apt update
sudo apt upgrade
sudo apt install python3
sudo apt install python3-pip
```

Install dependencies for this app.

```bash
python3 -m pip install python-chess pygame
```

Run the app.

```bash
python3 engine.py
```

## Heuristic options

- pieceCount (default)
  - This is the traditional count of points (pawns are 1, knights/bishops are 3, rooks are 5, queens are 9)
- random
- worstPossibleMove (opposite of pieceCount)
