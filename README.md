# Gomoku AI Game

This Python project implements the classic Gomoku game, where a player competes against an AI to achieve five consecutive stones on an 8x8 board. The AI uses strategic scoring functions to make optimal moves, while the program ensures valid gameplay, detects win conditions, and provides game state analysis.

## Features

### Core Gameplay
- **Player vs AI**: Compete against a computer opponent. The player uses white stones (`w`), and the AI uses black stones (`b`).
- **Win Detection**: Automatically detects winning conditions (five in a row) and announces the winner:
  - "Black won" (AI victory)
  - "White won" (player victory)
  - "Draw" (if the board is full and no winner is declared)
- **Interactive Input**: The player inputs move coordinates to place their stones.

### AI Opponent
- **Heuristic-Based AI**:
  - Evaluates board states using open and semi-open row detection.
  - Strategically blocks the player’s winning sequences.
  - Maximizes its own chances of victory by prioritizing high-value moves.
- **Move Scoring**: The AI scores potential moves based on the number and type of open/semi-open rows of length 2, 3, 4, and 5.

### Board Analysis
- **Real-Time Board Updates**: The board is displayed after every move, showing the current game state.
- **Game State Analysis**:
  - Tracks open and semi-open rows of length 2, 3, 4, and 5 for both the player and the AI.
  - Provides insights into strategic opportunities and threats.

## How to Play

1. Clone this repository:
   ```bash
   git clone https://github.com/yourusername/gomoku.git


2. Run the program: python gomoku.py

3. Gameplay Instructions:
	•	The AI starts by placing a black stone (b) in the center of the board.
	•	The player is prompted to input their move coordinates (y and x).
	•	The game alternates turns until:
	•	A player achieves five in a row.
	•	The board is full, resulting in a draw.
	•	The result is displayed at the end of the game.

## Example Gameplay

Starting Board
*0|1|2|3|4|5|6|7*
0 | | | | | | | | *
1 | | | | | | | | *
2 | | | | | | | | *
3 | | | | | | | | *
4 | | | | | | | | *
5 | | | | | | | | *
6 | | | | | | | | *
7 | | | | | | | | *
******************* 

After a Few Moves

*0|1|2|3|4|5|6|7*
0 | | | | | |b| | *
1 | | | | | | | | *
2 | | | | | | | | *
3 | | | | | |w| | *
4 | | | | | | | | *
5 | | | | |b|w| | *
6 | | | | | | | | *
7 | | | | | | | | *
*******************

## Functions Overview

### Game Mechanics
- **`play_gomoku(board_size: int)`**: Main function to initialize and run the game.
- **`is_win(board: list) -> str`**: Checks if a player has won or if the game is a draw.
- **`make_empty_board(size: int) -> list`**: Creates an empty game board.
- **`print_board(board: list)`**: Prints the current board state.

### AI Logic
- **`search_max(board: list) -> tuple`**: Determines the AI’s optimal move by evaluating the board state.
- **`score(board: list) -> int`**: Calculates a heuristic score for the current board state based on open and semi-open rows.

### Board Analysis
- **`analysis(board: list)`**: Analyzes the board to count open and semi-open rows for both players.
- **`detect_rows(board: list, col: str, length: int) -> tuple`**: Counts open and semi-open rows of a given length for a specified player.
- **`detect_row(board: list, col: str, y_start: int, x_start: int, length: int, d_y: int, d_x: int) -> tuple`**: Evaluates rows in specific directions (horizontal, vertical, diagonal).

## Testing

The program includes several test functions to validate functionality:

- **`test_is_empty()`**: Verifies whether the board is empty.
- **`test_is_bounded()`**: Tests if a sequence of stones is bounded (open, semi-open, or closed).
- **`test_detect_row()`**: Validates row detection logic.
- **`test_detect_rows()`**: Ensures accurate counting of rows across the board.
- **`test_search_max()`**: Checks the AI’s ability to find optimal moves.

  
## Future Enhancements
- Expand board size and rules for flexibility.
- Incorporate a GUI for enhanced user experience.

