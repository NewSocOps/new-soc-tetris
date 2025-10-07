# SPDX-License-Identifier: Apache-2.0 OR MIT

"""
AI Agent module for AI vs AI Tetris Arena.
Implements different AI strategies: greedy, aggressive, defensive.
"""

import random
import time
from typing import Tuple, Optional
from game_engine import GameBoard, Tetromino
from bank import FigureBank


class AIAgent:
    """Base class for AI agents."""
    
    def __init__(self, name: str, strategy: str = "greedy"):
        self.name = name
        self.strategy = strategy
        self.decision_times = []
    
    def decide_placement(self, board: GameBoard, piece: Tetromino) -> Tuple[int, int, int]:
        """
        Decide where to place a piece.
        Returns (x, y, rotations) tuple.
        """
        start_time = time.time()
        
        best_position = None
        best_score = float('-inf')
        
        # Try all rotations
        for rotation in range(4):
            piece_copy = Tetromino(piece.type)
            for _ in range(rotation):
                piece_copy.rotate()
            
            # Try all x positions
            for x in range(board.width - piece_copy.get_width() + 1):
                # Drop piece to lowest valid position
                y = 0
                while y < board.height and board.can_place(piece_copy, x, y):
                    y += 1
                y -= 1  # Back up to last valid position
                
                if y >= 0 and board.can_place(piece_copy, x, y):
                    # Evaluate this position
                    score = self._evaluate_position(board, piece_copy, x, y)
                    if score > best_score:
                        best_score = score
                        best_position = (x, y, rotation)
        
        decision_time = time.time() - start_time
        self.decision_times.append(decision_time)
        
        if best_position:
            return best_position
        
        # Fallback: place at center top
        return (board.width // 2, 0, 0)
    
    def _evaluate_position(self, board: GameBoard, piece: Tetromino, x: int, y: int) -> float:
        """Evaluate a potential piece placement."""
        # Create a copy of the board to test
        test_board = GameBoard(board.width, board.height)
        test_board.grid = [row[:] for row in board.grid]
        
        # Place the piece
        test_board.place_piece(piece, x, y)
        
        # Calculate metrics
        max_height = test_board.get_max_height()
        heights = test_board.get_height_map()
        
        # Calculate height variance (bumpiness)
        bumpiness = sum(abs(heights[i] - heights[i+1]) 
                       for i in range(len(heights) - 1))
        
        # Count holes (empty cells with filled cells above)
        holes = 0
        for col_x in range(board.width):
            found_block = False
            for row_y in range(board.height):
                if test_board.grid[row_y][col_x]:
                    found_block = True
                elif found_block:
                    holes += 1
        
        # Strategy-specific scoring
        if self.strategy == "greedy":
            # Minimize height, holes, and bumpiness
            score = -max_height * 2 - holes * 5 - bumpiness
        elif self.strategy == "defensive":
            # Prioritize stability and low height
            score = -max_height * 3 - holes * 10 - bumpiness * 2
        elif self.strategy == "aggressive":
            # Allow higher stacks if it leads to line clears
            lines_cleared = self._count_potential_lines(test_board)
            score = lines_cleared * 100 - max_height - holes * 3
        else:
            score = -max_height - holes
        
        return score
    
    def _count_potential_lines(self, board: GameBoard) -> int:
        """Count how many lines would be cleared."""
        count = 0
        for y in range(board.height):
            if all(board.grid[y]):
                count += 1
        return count
    
    def choose_attack_piece(self, bank: FigureBank) -> Optional[str]:
        """
        Choose a piece to send to the opponent.
        Returns the piece type or None if bank is empty.
        """
        available = bank.get_available_pieces()
        if not available:
            return None
        
        if self.strategy == "aggressive":
            # Send difficult pieces (I, O, S, Z are easier; T, L, J are harder)
            difficult_pieces = ['T', 'L', 'J']
            difficult_available = [p for p in difficult_pieces if p in available]
            if difficult_available:
                return random.choice(difficult_available)
        elif self.strategy == "defensive":
            # Send easier pieces to conserve difficult ones
            easy_pieces = ['I', 'O']
            easy_available = [p for p in easy_pieces if p in available]
            if easy_available:
                return random.choice(easy_available)
        
        # Default: random choice
        return random.choice(available)
    
    def get_average_decision_time(self) -> float:
        """Get the average time taken for decisions."""
        if not self.decision_times:
            return 0.0
        return sum(self.decision_times) / len(self.decision_times)
