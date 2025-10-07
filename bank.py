# SPDX-License-Identifier: Apache-2.0 OR MIT

"""
Figure Bank module for AI vs AI Tetris Arena.
Manages the shared pool of tetromino pieces.
"""

import random
from typing import Optional, Dict, List

TETROMINO_TYPES = ['I', 'O', 'T', 'S', 'Z', 'L', 'J']


class FigureBank:
    """Manages a finite pool of tetromino pieces."""
    
    def __init__(self, initial_count: int = 15):
        """Initialize the bank with a specified count of each piece type."""
        self.bank = {piece_type: initial_count for piece_type in TETROMINO_TYPES}
        self.initial_count = initial_count
    
    def get_piece(self, piece_type: str) -> bool:
        """
        Attempt to draw a piece from the bank.
        Returns True if successful, False if the piece is unavailable.
        """
        if piece_type not in self.bank:
            return False
        
        if self.bank[piece_type] > 0:
            self.bank[piece_type] -= 1
            return True
        
        return False
    
    def is_available(self, piece_type: str) -> bool:
        """Check if a piece type is available in the bank."""
        return piece_type in self.bank and self.bank[piece_type] > 0
    
    def get_available_pieces(self) -> List[str]:
        """Get a list of all available piece types."""
        return [piece_type for piece_type in TETROMINO_TYPES 
                if self.bank[piece_type] > 0]
    
    def is_empty(self) -> bool:
        """Check if the bank is completely empty."""
        return all(count == 0 for count in self.bank.values())
    
    def get_random_available(self) -> Optional[str]:
        """Get a random available piece type, or None if bank is empty."""
        available = self.get_available_pieces()
        if available:
            return random.choice(available)
        return None
    
    def get_state(self) -> Dict[str, int]:
        """Get the current state of the bank."""
        return self.bank.copy()
    
    def get_total_remaining(self) -> int:
        """Get the total number of pieces remaining."""
        return sum(self.bank.values())
    
    def to_string(self) -> str:
        """Convert bank state to ASCII string."""
        lines = ["FIGURE BANK:"]
        for piece_type in TETROMINO_TYPES:
            count = self.bank[piece_type]
            bar = "|" * count
            lines.append(f"{piece_type}: {bar} ({count})")
        lines.append(f"Total: {self.get_total_remaining()}")
        return "\n".join(lines)
