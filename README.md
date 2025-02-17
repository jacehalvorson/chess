# Chess Engine

- [Chess Engine](#chess-engine)
  - [How to Run](#how-to-run)
  - [Prerequisites](#prerequisites)
    - [Install Git](#install-git)
    - [Clone this Repository](#clone-this-repository)
    - [Install Python](#install-python)
      - [Windows](#windows)
      - [Linux](#linux)
    - [Install Stockfish (Optional)](#install-stockfish-optional)
  - [Heuristic options](#heuristic-options)

Play Chess against a minimax algorithm.

Or watch it try to hold its own against Stockfish. Currently it plays againast a Stockfish limited to 1320 and it gets crushed. Improvements are in progress for a better heuristic, potentially incorporating neural networks.

## How to Run

```bash
python3 engine.py
```

> Note: Follow the steps in the [Prerequisites](#prerequisites) section first.

Usage information:

```text
usage: python3 engine.py [-h] [--ai] [--color COLOR] [--heuristic HEURISTIC]

Play chess against an AI or watch 2 AIs play against each other

options:
  -h, --help            show this help message and exit
  --stockfish, -s       Instead of playing against AI, pin 2 of them against each other and watch them play
  --color, -c COLOR     Choose the color on the bottom of the screen (white or black)
  --heuristic HEURISTIC
                        Choose the AI's method of evaluating the board state. Options: pieceCount, random, worstPossibleMove
```

## Prerequisites

### Install Git

Visit [https://git-scm.com/downloads](https://git-scm.com/downloads) to install Git on any operating system. If you're using Linux, you can simply run `sudo apt install git` instead.

Open Git Bash (terminal).

### Clone this Repository

```bash
git clone https://github.com/jacehalvorson/chess.git
cd chess
```

### Install Python

#### Windows

If you don't have Python and pip installed, run this to open the Microsoft Store and install Python 3. Then install pip.

```bash
python3
# Follow prompts opened by Microsoft Store
python3 -m ensurepip --upgrade
```

This app requires a few packages. Install them with this command:

```bash
python3 -m pip install python-chess pygame
```

#### Linux

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

### Install Stockfish (Optional)

Download from https://stockfishchess.org/download/ and copy the *.exe file into this repository, renaming it to 'stockfish.exe'

## Heuristic options

- pieceCount (default)
  - This is the traditional count of points (pawns are 1, knights/bishops are 3, rooks are 5, queens are 9)
- random
- worstPossibleMove (opposite of pieceCount)
