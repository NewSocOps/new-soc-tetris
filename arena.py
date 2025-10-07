# SPDX-License-Identifier: Apache-2.0 OR MIT

"""
Arena module for AI vs AI Tetris Arena.
Orchestrates matches between two AI agents.
"""

import json
import time
from typing import Dict, List, Optional
from game_engine import GameBoard, Tetromino
from bank import FigureBank
from ai_agent import AIAgent


class MatchLog:
    """Records match events for analysis."""
    
    def __init__(self):
        self.events = []
        self.start_time = time.time()
    
    def log_turn(self, turn: int, player: str, piece_type: str, 
                 placement: tuple, lines_cleared: int, decision_time: float,
                 bank_state: Dict, attack_piece: Optional[str]):
        """Log a single turn."""
        event = {
            "turn": turn,
            "player": player,
            "piece_type": piece_type,
            "placement": {"x": placement[0], "y": placement[1], "rotation": placement[2]},
            "lines_cleared": lines_cleared,
            "decision_time": decision_time,
            "bank_state": bank_state,
            "attack_piece": attack_piece,
            "timestamp": time.time() - self.start_time
        }
        self.events.append(event)
    
    def log_game_over(self, winner: str, ai1_score: int, ai2_score: int,
                     ai1_lines: int, ai2_lines: int):
        """Log the game over event."""
        event = {
            "event": "game_over",
            "winner": winner,
            "scores": {"ai1": ai1_score, "ai2": ai2_score},
            "lines_cleared": {"ai1": ai1_lines, "ai2": ai2_lines},
            "timestamp": time.time() - self.start_time
        }
        self.events.append(event)
    
    def save_to_file(self, filename: str = "match_log.json"):
        """Save the log to a JSON file."""
        with open(filename, 'w') as f:
            json.dump(self.events, f, indent=2)


class Arena:
    """Manages AI vs AI Tetris matches."""
    
    def __init__(self, ai1: AIAgent, ai2: AIAgent, bank: FigureBank):
        self.ai1 = ai1
        self.ai2 = ai2
        self.board1 = GameBoard()
        self.board2 = GameBoard()
        self.bank = bank
        self.log = MatchLog()
        self.turn = 0
        self.current_piece_ai1 = None
        self.current_piece_ai2 = None
        self.garbage_queue_ai1 = 0
        self.garbage_queue_ai2 = 0
    
    def _get_next_piece(self) -> str:
        """Get the next piece from bank or random generator."""
        piece_type = self.bank.get_random_available()
        if piece_type:
            self.bank.get_piece(piece_type)
            return piece_type
        else:
            # Fallback to random generator
            import random
            from bank import TETROMINO_TYPES
            return random.choice(TETROMINO_TYPES)
    
    def play_turn(self, ai: AIAgent, board: GameBoard, piece_type: str) -> tuple:
        """
        Play a single turn for an AI.
        Returns (lines_cleared, decision_time, attack_piece).
        """
        piece = Tetromino(piece_type)
        
        # AI decides placement
        x, y, rotations = ai.decide_placement(board, piece)
        
        # Rotate piece
        for _ in range(rotations):
            piece.rotate()
        
        # Place piece
        if board.can_place(piece, x, y):
            board.place_piece(piece, x, y)
        else:
            # If can't place, game over
            board.game_over = True
            return 0, 0.0, None
        
        # Clear lines
        lines_cleared = board.clear_lines()
        
        # Choose attack piece
        attack_piece = None
        if lines_cleared > 0:
            attack_piece = ai.choose_attack_piece(self.bank)
        
        decision_time = ai.decision_times[-1] if ai.decision_times else 0.0
        
        return lines_cleared, decision_time, attack_piece
    
    def run_match(self, max_turns: int = 1000) -> str:
        """
        Run a complete match between the two AIs.
        Returns the name of the winner.
        """
        # Initialize first pieces
        self.current_piece_ai1 = self._get_next_piece()
        self.current_piece_ai2 = self._get_next_piece()
        
        while self.turn < max_turns:
            self.turn += 1
            
            # Process garbage for AI1
            if self.garbage_queue_ai1 > 0:
                self.board1.add_garbage_lines(self.garbage_queue_ai1)
                self.garbage_queue_ai1 = 0
            
            # AI1's turn
            lines1, time1, attack1 = self.play_turn(
                self.ai1, self.board1, self.current_piece_ai1
            )
            
            self.log.log_turn(
                self.turn, self.ai1.name, self.current_piece_ai1,
                (0, 0, 0), lines1, time1, self.bank.get_state(), attack1
            )
            
            # Send garbage to AI2
            if lines1 > 0:
                self.garbage_queue_ai2 += lines1
            
            # Update AI1's piece
            if attack1 and self.bank.is_available(attack1):
                self.current_piece_ai1 = attack1
                self.bank.get_piece(attack1)
            else:
                self.current_piece_ai1 = self._get_next_piece()
            
            # Check if AI1 lost
            if self.board1.is_game_over():
                self.log.log_game_over(
                    self.ai2.name, self.board1.score, self.board2.score,
                    self.board1.lines_cleared, self.board2.lines_cleared
                )
                return self.ai2.name
            
            # Process garbage for AI2
            if self.garbage_queue_ai2 > 0:
                self.board2.add_garbage_lines(self.garbage_queue_ai2)
                self.garbage_queue_ai2 = 0
            
            # AI2's turn
            lines2, time2, attack2 = self.play_turn(
                self.ai2, self.board2, self.current_piece_ai2
            )
            
            self.log.log_turn(
                self.turn, self.ai2.name, self.current_piece_ai2,
                (0, 0, 0), lines2, time2, self.bank.get_state(), attack2
            )
            
            # Send garbage to AI1
            if lines2 > 0:
                self.garbage_queue_ai1 += lines2
            
            # Update AI2's piece
            if attack2 and self.bank.is_available(attack2):
                self.current_piece_ai2 = attack2
                self.bank.get_piece(attack2)
            else:
                self.current_piece_ai2 = self._get_next_piece()
            
            # Check if AI2 lost
            if self.board2.is_game_over():
                self.log.log_game_over(
                    self.ai1.name, self.board1.score, self.board2.score,
                    self.board1.lines_cleared, self.board2.lines_cleared
                )
                return self.ai1.name
        
        # Max turns reached, determine winner by score
        winner = self.ai1.name if self.board1.score > self.board2.score else self.ai2.name
        self.log.log_game_over(
            winner, self.board1.score, self.board2.score,
            self.board1.lines_cleared, self.board2.lines_cleared
        )
        return winner
    
    def get_state(self) -> Dict:
        """Get the current state of the arena."""
        return {
            "turn": self.turn,
            "ai1": {
                "name": self.ai1.name,
                "score": self.board1.score,
                "lines_cleared": self.board1.lines_cleared,
                "current_piece": self.current_piece_ai1
            },
            "ai2": {
                "name": self.ai2.name,
                "score": self.board2.score,
                "lines_cleared": self.board2.lines_cleared,
                "current_piece": self.current_piece_ai2
            },
            "bank": self.bank.get_state()
        }
