# SPDX-License-Identifier: Apache-2.0 OR MIT

"""
Main entry point for AI vs AI Tetris Arena.
Supports both pygame visualization and ASCII mode.
"""

import argparse
import sys
import time

try:
    import pygame
    PYGAME_AVAILABLE = True
except ImportError:
    PYGAME_AVAILABLE = False

from game_engine import GameBoard, Tetromino
from bank import FigureBank
from ai_agent import AIAgent
from arena import Arena


def run_ascii_mode(ai1_strategy: str = "greedy", ai2_strategy: str = "aggressive"):
    """Run the game in ASCII mode (headless)."""
    print("=" * 60)
    print("AI vs AI TETRIS ARENA - ASCII MODE")
    print("=" * 60)
    
    # Initialize components
    bank = FigureBank(initial_count=15)
    ai1 = AIAgent("AI-1", strategy=ai1_strategy)
    ai2 = AIAgent("AI-2", strategy=ai2_strategy)
    arena = Arena(ai1, ai2, bank)
    
    print(f"\nAI-1 Strategy: {ai1_strategy}")
    print(f"AI-2 Strategy: {ai2_strategy}")
    print(f"\nStarting match...\n")
    
    # Run match
    winner = arena.run_match(max_turns=100)
    
    # Display results
    print("\n" + "=" * 60)
    print("MATCH COMPLETE")
    print("=" * 60)
    print(f"\nWinner: {winner}")
    print(f"\nFinal Scores:")
    print(f"  AI-1: {arena.board1.score} (Lines: {arena.board1.lines_cleared})")
    print(f"  AI-2: {arena.board2.score} (Lines: {arena.board2.lines_cleared})")
    print(f"\nAverage Decision Times:")
    print(f"  AI-1: {ai1.get_average_decision_time():.4f}s")
    print(f"  AI-2: {ai2.get_average_decision_time():.4f}s")
    print(f"\nBank State:")
    print(bank.to_string())
    
    # Save log
    arena.log.save_to_file("match_log.json")
    print("\nMatch log saved to match_log.json")
    
    # Display final boards
    print("\n" + "=" * 60)
    print("FINAL BOARDS")
    print("=" * 60)
    print("\nAI-1 Board:")
    print(arena.board1.to_string())
    print(f"\nAI-2 Board:")
    print(arena.board2.to_string())


def run_pygame_mode(ai1_strategy: str = "greedy", ai2_strategy: str = "aggressive"):
    """Run the game with pygame visualization."""
    if not PYGAME_AVAILABLE:
        print("ERROR: pygame is not installed. Install it with: pip install pygame")
        print("Falling back to ASCII mode...")
        run_ascii_mode(ai1_strategy, ai2_strategy)
        return
    
    # Initialize pygame
    pygame.init()
    
    # Constants
    CELL_SIZE = 25
    BOARD_WIDTH = 10
    BOARD_HEIGHT = 20
    INFO_WIDTH = 300
    SCREEN_WIDTH = BOARD_WIDTH * CELL_SIZE * 2 + INFO_WIDTH + 60
    SCREEN_HEIGHT = BOARD_HEIGHT * CELL_SIZE + 100
    
    # Colors
    BLACK = (0, 0, 0)
    WHITE = (255, 255, 255)
    GRAY = (128, 128, 128)
    RED = (255, 0, 0)
    GREEN = (0, 255, 0)
    BLUE = (0, 0, 255)
    CYAN = (0, 255, 255)
    
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("AI vs AI Tetris Arena")
    clock = pygame.time.Clock()
    font = pygame.font.Font(None, 24)
    small_font = pygame.font.Font(None, 18)
    
    # Initialize components
    bank = FigureBank(initial_count=15)
    ai1 = AIAgent("AI-1", strategy=ai1_strategy)
    ai2 = AIAgent("AI-2", strategy=ai2_strategy)
    arena = Arena(ai1, ai2, bank)
    
    # Initialize first pieces
    arena.current_piece_ai1 = arena._get_next_piece()
    arena.current_piece_ai2 = arena._get_next_piece()
    
    running = True
    paused = False
    game_over = False
    winner = None
    turn_delay = 500  # milliseconds between turns
    last_turn_time = pygame.time.get_ticks()
    
    def draw_board(board: GameBoard, offset_x: int, offset_y: int):
        """Draw a game board."""
        # Draw grid
        for y in range(board.height):
            for x in range(board.width):
                rect = pygame.Rect(
                    offset_x + x * CELL_SIZE,
                    offset_y + y * CELL_SIZE,
                    CELL_SIZE, CELL_SIZE
                )
                if board.grid[y][x]:
                    pygame.draw.rect(screen, CYAN, rect)
                pygame.draw.rect(screen, GRAY, rect, 1)
    
    def draw_info():
        """Draw game information."""
        info_x = BOARD_WIDTH * CELL_SIZE * 2 + 40
        y_offset = 50
        
        # Title
        title = font.render("AI vs AI Tetris", True, WHITE)
        screen.blit(title, (info_x, 10))
        
        # AI-1 Info
        text = font.render("AI-1 (Left)", True, GREEN)
        screen.blit(text, (info_x, y_offset))
        y_offset += 30
        
        text = small_font.render(f"Strategy: {ai1.strategy}", True, WHITE)
        screen.blit(text, (info_x, y_offset))
        y_offset += 25
        
        text = small_font.render(f"Score: {arena.board1.score}", True, WHITE)
        screen.blit(text, (info_x, y_offset))
        y_offset += 20
        
        text = small_font.render(f"Lines: {arena.board1.lines_cleared}", True, WHITE)
        screen.blit(text, (info_x, y_offset))
        y_offset += 30
        
        # AI-2 Info
        text = font.render("AI-2 (Right)", True, RED)
        screen.blit(text, (info_x, y_offset))
        y_offset += 30
        
        text = small_font.render(f"Strategy: {ai2.strategy}", True, WHITE)
        screen.blit(text, (info_x, y_offset))
        y_offset += 25
        
        text = small_font.render(f"Score: {arena.board2.score}", True, WHITE)
        screen.blit(text, (info_x, y_offset))
        y_offset += 20
        
        text = small_font.render(f"Lines: {arena.board2.lines_cleared}", True, WHITE)
        screen.blit(text, (info_x, y_offset))
        y_offset += 30
        
        # Bank Info
        text = font.render("Bank Status", True, WHITE)
        screen.blit(text, (info_x, y_offset))
        y_offset += 30
        
        text = small_font.render(f"Remaining: {bank.get_total_remaining()}", True, WHITE)
        screen.blit(text, (info_x, y_offset))
        y_offset += 25
        
        # Turn info
        text = small_font.render(f"Turn: {arena.turn}", True, WHITE)
        screen.blit(text, (info_x, y_offset))
    
    # Main game loop
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    paused = not paused
                elif event.key == pygame.K_ESCAPE:
                    running = False
        
        # Update game state
        if not paused and not game_over:
            current_time = pygame.time.get_ticks()
            if current_time - last_turn_time > turn_delay:
                last_turn_time = current_time
                arena.turn += 1
                
                # Process AI1 turn
                if arena.garbage_queue_ai1 > 0:
                    arena.board1.add_garbage_lines(arena.garbage_queue_ai1)
                    arena.garbage_queue_ai1 = 0
                
                lines1, time1, attack1 = arena.play_turn(
                    ai1, arena.board1, arena.current_piece_ai1
                )
                
                if lines1 > 0:
                    arena.garbage_queue_ai2 += lines1
                
                if attack1 and bank.is_available(attack1):
                    arena.current_piece_ai1 = attack1
                    bank.get_piece(attack1)
                else:
                    arena.current_piece_ai1 = arena._get_next_piece()
                
                if arena.board1.is_game_over():
                    game_over = True
                    winner = "AI-2"
                
                # Process AI2 turn
                if not game_over:
                    if arena.garbage_queue_ai2 > 0:
                        arena.board2.add_garbage_lines(arena.garbage_queue_ai2)
                        arena.garbage_queue_ai2 = 0
                    
                    lines2, time2, attack2 = arena.play_turn(
                        ai2, arena.board2, arena.current_piece_ai2
                    )
                    
                    if lines2 > 0:
                        arena.garbage_queue_ai1 += lines2
                    
                    if attack2 and bank.is_available(attack2):
                        arena.current_piece_ai2 = attack2
                        bank.get_piece(attack2)
                    else:
                        arena.current_piece_ai2 = arena._get_next_piece()
                    
                    if arena.board2.is_game_over():
                        game_over = True
                        winner = "AI-1"
                
                # Check turn limit
                if arena.turn >= 1000:
                    game_over = True
                    winner = "AI-1" if arena.board1.score > arena.board2.score else "AI-2"
        
        # Draw everything
        screen.fill(BLACK)
        
        # Draw boards
        draw_board(arena.board1, 20, 50)
        draw_board(arena.board2, BOARD_WIDTH * CELL_SIZE + 40, 50)
        
        # Draw info
        draw_info()
        
        # Draw labels
        label1 = font.render("AI-1", True, GREEN)
        screen.blit(label1, (20, 20))
        
        label2 = font.render("AI-2", True, RED)
        screen.blit(label2, (BOARD_WIDTH * CELL_SIZE + 40, 20))
        
        # Draw game over message
        if game_over:
            overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
            overlay.set_alpha(128)
            overlay.fill(BLACK)
            screen.blit(overlay, (0, 0))
            
            text = font.render(f"GAME OVER - Winner: {winner}!", True, WHITE)
            text_rect = text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
            screen.blit(text, text_rect)
            
            text2 = small_font.render("Press ESC to exit", True, WHITE)
            text2_rect = text2.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 40))
            screen.blit(text2, text2_rect)
        
        # Draw pause message
        if paused:
            text = font.render("PAUSED - Press SPACE to continue", True, WHITE)
            text_rect = text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT - 30))
            screen.blit(text, text_rect)
        
        pygame.display.flip()
        clock.tick(60)
    
    # Save log before quitting
    arena.log.save_to_file("match_log.json")
    pygame.quit()


def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(description="AI vs AI Tetris Arena")
    parser.add_argument(
        "--ascii", 
        action="store_true",
        help="Run in ASCII mode (no pygame)"
    )
    parser.add_argument(
        "--ai1",
        type=str,
        default="greedy",
        choices=["greedy", "aggressive", "defensive"],
        help="Strategy for AI-1 (default: greedy)"
    )
    parser.add_argument(
        "--ai2",
        type=str,
        default="aggressive",
        choices=["greedy", "aggressive", "defensive"],
        help="Strategy for AI-2 (default: aggressive)"
    )
    
    args = parser.parse_args()
    
    if args.ascii:
        run_ascii_mode(args.ai1, args.ai2)
    else:
        run_pygame_mode(args.ai1, args.ai2)


if __name__ == "__main__":
    main()
