You are tasked with creating a new open-source project called
"AI vs AI Tetris Arena with Figure Bank".

## Project Goals
- Implement a Tetris-style competitive game where two AI agents play against each other.
- Introduce a shared "Figure Bank" mechanic: a limited pool of tetrominoes from which AIs must draw and send pieces to their opponent.
- Support multiple AI strategies (aggressive, defensive, greedy).
- Provide both visualization (pygame) and a text-based ASCII mode for testing.

## Core Features
1. **Game Engine (game_engine.py)**
   - Classic Tetris rules on a 10x20 grid.
   - Piece placement, line clearing, scoring.
   - Garbage line injection when opponent clears lines.

2. **Figure Bank (bank.py)**
   - Initialize a finite pool of tetrominoes (e.g., 15 of each type).
   - Track remaining pieces.
   - Allow AI to select a piece from the bank to send to the opponent.
   - If the bank is empty, fall back to a random generator.

3. **AI Agents (ai_agent.py)**
   - Implement at least three strategies:
     - Greedy (minimize stack height).
     - Aggressive (maximize attack by sending difficult pieces).
     - Defensive (prioritize survival).
   - Each AI must decide placement and attack within a time limit.

4. **Arena (arena.py)**
   - Run matches between two AI agents.
   - Synchronize turns.
   - Track scores, lines cleared, garbage sent, and bank usage.
   - Log all moves and states to JSON for analysis.

5. **Main Entry (main.py)**
   - Provide a pygame visualization with two side-by-side boards.
   - Show the current state of the Figure Bank.
   - Display scores and statistics.
   - Support ASCII mode for headless testing.

## Visualization
- Two boards side by side (left = AI-1, right = AI-2).
- Bank display: remaining counts of each tetromino.
- Scoreboard: points, lines cleared, garbage sent.

## Logging
- JSON logs with:
  - Moves taken.
  - Time per decision.
  - Bank state after each turn.
  - Attack effectiveness.

## Licensing
- The project must include **dual licensing**:
  - `LICENSE-APACHE.md` with Apache License 2.0.
  - `LICENSE-MIT.md` with MIT License.
- Add a `NOTICE` file with attribution: "Copyright (c) 2025 Nikolay & Microsoft Copilot".
- In `README.md`, include a "License" section stating:

This project is licensed under either Apache License 2.0 or MIT License, at your option. SPDX: Apache-2.0 OR MIT

- Add SPDX headers (`# SPDX-License-Identifier: Apache-2.0 OR MIT`) to source files.

## Deliverables
- A working Python project with the above modules.
- A `README.md` describing:
- Game concept and rules.
- How to run the game (pygame and ASCII modes).
- How to switch AI strategies.
- License section with dual licensing.
- Example ASCII illustrations of the board and bank in the README.

## Stretch Goals (optional)
- Add replay saving and playback.
- Add configurable AI parameters.
- Add tournament mode (multiple matches with statistics).
