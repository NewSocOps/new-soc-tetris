# SPDX-License-Identifier: Apache-2.0 OR MIT

"""
Game Engine module for AI vs AI Tetris Arena.
Implements classic Tetris rules on a 10x20 grid.
"""

import random
from typing import List, Tuple, Optional

# Tetromino shapes (4x4 grid representation)
SHAPES = {
    'I': [[1, 1, 1, 1]],
    'O': [[1, 1], [1, 1]],
    'T': [[0, 1, 0], [1, 1, 1]],
    'S': [[0, 1, 1], [1, 1, 0]],
    'Z': [[1, 1, 0], [0, 1, 1]],
    'L': [[1, 0], [1, 0], [1, 1]],
    'J': [[0, 1], [0, 1], [1, 1]]
}


class Tetromino:
    """Represents a Tetris piece."""
    
    def __init__(self, shape_type: str):
        self.type = shape_type
        self.shape = SHAPES[shape_type]
        self.rotation = 0
    
    def rotate(self):
        """Rotate the piece 90 degrees clockwise."""
        self.shape = [list(row) for row in zip(*self.shape[::-1])]
        self.rotation = (self.rotation + 1) % 4
    
    def get_width(self) -> int:
        """Get the width of the current shape."""
        return len(self.shape[0]) if self.shape else 0
    
    def get_height(self) -> int:
        """Get the height of the current shape."""
        return len(self.shape)


class GameBoard:
    """Represents a Tetris game board."""
    
    def __init__(self, width: int = 10, height: int = 20):
        self.width = width
        self.height = height
        self.grid = [[0 for _ in range(width)] for _ in range(height)]
        self.score = 0
        self.lines_cleared = 0
        self.game_over = False
    
    def can_place(self, piece: Tetromino, x: int, y: int) -> bool:
        """Check if a piece can be placed at the given position."""
        for row_idx, row in enumerate(piece.shape):
            for col_idx, cell in enumerate(row):
                if cell:
                    board_y = y + row_idx
                    board_x = x + col_idx
                    
                    if (board_x < 0 or board_x >= self.width or
                        board_y < 0 or board_y >= self.height):
                        return False
                    
                    if self.grid[board_y][board_x]:
                        return False
        
        return True
    
    def place_piece(self, piece: Tetromino, x: int, y: int):
        """Place a piece on the board."""
        for row_idx, row in enumerate(piece.shape):
            for col_idx, cell in enumerate(row):
                if cell:
                    board_y = y + row_idx
                    board_x = x + col_idx
                    if 0 <= board_y < self.height and 0 <= board_x < self.width:
                        self.grid[board_y][board_x] = 1
    
    def clear_lines(self) -> int:
        """Clear completed lines and return the number cleared."""
        lines_to_clear = []
        
        for y in range(self.height):
            if all(self.grid[y]):
                lines_to_clear.append(y)
        
        for y in lines_to_clear:
            del self.grid[y]
            self.grid.insert(0, [0 for _ in range(self.width)])
        
        num_cleared = len(lines_to_clear)
        if num_cleared > 0:
            self.lines_cleared += num_cleared
            # Score: 1=100, 2=300, 3=500, 4=800
            score_table = {1: 100, 2: 300, 3: 500, 4: 800}
            self.score += score_table.get(num_cleared, num_cleared * 100)
        
        return num_cleared
    
    def add_garbage_lines(self, num_lines: int):
        """Add garbage lines to the bottom of the board."""
        for _ in range(num_lines):
            # Remove top line
            self.grid.pop(0)
            # Add garbage line at bottom with one random hole
            garbage_line = [1] * self.width
            hole_position = random.randint(0, self.width - 1)
            garbage_line[hole_position] = 0
            self.grid.append(garbage_line)
    
    def is_game_over(self) -> bool:
        """Check if the game is over (top row has blocks)."""
        return any(self.grid[0])
    
    def get_height_map(self) -> List[int]:
        """Get the height of each column."""
        heights = []
        for x in range(self.width):
            height = 0
            for y in range(self.height):
                if self.grid[y][x]:
                    height = self.height - y
                    break
            heights.append(height)
        return heights
    
    def get_max_height(self) -> int:
        """Get the maximum height of any column."""
        heights = self.get_height_map()
        return max(heights) if heights else 0
    
    def to_string(self) -> str:
        """Convert board to ASCII string."""
        lines = []
        lines.append("+" + "-" * self.width + "+")
        for row in self.grid:
            line = "|"
            for cell in row:
                line += "█" if cell else " "
            line += "|"
            lines.append(line)
        lines.append("+" + "-" * self.width + "+")
        return "\n".join(lines)
