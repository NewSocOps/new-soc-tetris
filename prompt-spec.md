# AI vs AI Tetris Arena with Figure Bank  
Spec Version: 1.1  
Target Model: GPT-5-Codex (code generation mode, Python 3.11)

## 0. Summary
Create an open-source Python project: a competitive Tetris arena where two autonomous AI agents play simultaneously on separate boards while sharing a finite "Figure Bank" of tetrominoes. The system includes: game engine, figure bank, multiple AI strategies (greedy / aggressive / defensive), arena orchestration, pygame visualization, ASCII/headless mode, JSON logging, dual licensing (Apache-2.0 OR MIT), and extensibility hooks.

---

## 1. Project Goals
1. Two-player AI vs AI competitive Tetris (independent 10x20 boards).
2. Shared, limited Figure Bank controlling tetromino availability.
3. Multiple pluggable AI strategies under a unified interface.
4. Two output modes: graphical (pygame) and ASCII (for CI / headless).
5. Detailed JSONL logging for offline analysis.
6. Clean architecture enabling additional agents, heuristics, or tournament modes.

---

## 2. Module Layout (Minimum Target)
```
project-root/
  arena.py            # Match orchestration
  bank.py             # FigureBank implementation
  game_engine.py      # Single-board Tetris logic
  ai_agent.py         # BaseAgent + Greedy, Aggressive, Defensive strategies
  main.py             # CLI entry point (pygame / ASCII)
  logging_utils.py    # JSONL logging helpers
  models.py           # Common dataclasses / typed structures (optional)
  replay.py           # (Stretch) Replay a logged match
  config.py           # (Optional) central configuration
  tests/              # Minimal tests (engine, bank, agents)
  README.md
  NOTICE
  LICENSE-MIT.md
  LICENSE-APACHE.md
  requirements.txt OR pyproject.toml
```

All Python source files MUST start with:
```
# SPDX-License-Identifier: Apache-2.0 OR MIT
```

---

## 3. Game Model

### 3.1 Board
- Width: 10
- Height: 20 visible rows (optional hidden spawn buffer 2–4 rows allowed internally).
- Representation: 2D array (list[list[str]]) or flat list; empty cell = ".".

### 3.2 Tetrominoes
Standard seven: I, O, T, S, Z, J, L.

Recommended shape storage (rotation variants):
```python
TETROMINO_SHAPES = {
  "I": [
    ["0000",
     "1111",
     "0000",
     "0000"],
    ["0010",
     "0010",
     "0010",
     "0010"]
  ],
  # ...
}
```

Rotation model:
- Provide all necessary rotations (4 for most, 2 for I/S/Z if simplified, 1 for O).
- Wall kicks: simplified (shift left/right if overlapping), not full SRS—document chosen approach.

### 3.3 Rules
- Gravity may be abstracted: agents decide final landing placement (hard drop simulation).
- Line clear: remove full rows, compress above content downward.
- Scoring (recommended constants):
  - 1 line: 100
  - 2 lines: 300
  - 3 lines: 500
  - 4 lines (Tetris): 800
- Garbage attack: (cleared_lines - 1) if >= 2; min 0. (Example: clearing 2 lines sends 1 garbage line.)
- Garbage line: random hole column, all other cells filled with a neutral block marker (e.g. "#").
- Top out: piece cannot spawn without overlap → player loses.

---

## 4. Figure Bank

### 4.1 Initialization
Default: 15 copies of each of the 7 tetromino types → total 105 entries.
Configurable via CLI (`--bank-count`) meaning “per-piece count”.

### 4.2 API (Minimum Contract)
```python
class FigureBank:
    def __init__(self, initial_counts: dict[str, int]): ...
    def remaining(self) -> dict[str, int]: ...
    def draw(self, kind: str) -> bool:
        """Attempt to consume a figure of given type; return True if successful."""
    def auto_select(self) -> str:
        """Select a figure automatically (random among remaining)."""
    def is_empty(self) -> bool: ...
```

### 4.3 Match Usage
Simplest base version:
- Each turn, each agent receives a piece from the bank (either chosen for itself or, if strategy allows, opponent piece selection).
- Aggressive strategy MAY choose a difficult piece for the opponent (e.g., S or Z) if bank still holds it.
- When bank is empty: fallback to a uniform random generator or classic 7-bag (document final choice).

---

## 5. AI Agents

### 5.1 Interface
```python
class BaseAgent:
    def decide(
        self,
        board_state,
        upcoming_bank_view: dict[str, int],
        time_limit_ms: int
    ) -> dict:
        """
        Returns dict:
        {
          "placement": {
              "x": int,
              "rotation": int,
              "hard_drop": bool
          },
          "select_for_opponent": "Z" | "S" | "I" | ... | None,
          "meta": {
              "heuristic_score": float | int | None,
              "reason": str | None,
              "comment": str | None,   # Short human-friendly explanation
              "timed_out": bool | None
          }
        }
        """
```

### 5.2 Strategies
- Greedy: minimize aggregate column heights (e.g., sum or variance).
- Aggressive: maximize disruption (fill awkward shapes, reduce opponent's flat surfaces).
- Defensive: minimize risk—avoid creating deep wells > 3, reduce holes and overhangs.

### 5.3 Time Management
Two independent parameters:
1. decision_time_limit_ms (internal computation budget; default 200 ms; CLI: `--time-limit-ms`).
2. turn_interval (presentation pacing delay after a full turn; default 0.0; CLI: `--turn-interval`).

If time exceeded:
- Fallback placement: first valid hard drop scanning column+rotation space.
- Mark `meta["timed_out"] = True`.
- Log actual measured duration anyway.

### 5.4 Human Commentary
Agents MAY include `"comment"` (≤ ~120 chars). ASCII/pygame modes show truncated comment (e.g., 80 chars). Logged verbatim in JSONL.

---

## 6. Arena

### 6.1 Responsibilities
1. Initialize boards, FigureBank, two agents.
2. Turn loop (synchronous):
   1. Determine each agent’s next piece (bank selection / aggressive override).
   2. Call `decide()` with time measurement.
   3. Validate placement (bounds, collision).
   4. Apply piece → update board state.
   5. Clear lines → compute score increment.
   6. Compute garbage → inject into opponent board.
   7. Log turn event.
   8. Render (if visualization enabled).
   9. Presentation delay: if `turn_interval > 0` sleep that duration.
3. Check top out (loss).
4. Terminate on victory, double-top-out (draw), or `--max-turns`.

### 6.2 End Conditions
- Win: opponent tops out first.
- Draw: simultaneous top out OR reaching max turns.
- Summary JSON object appended after final turn.

---

## 7. Logging (JSONL)

### 7.1 Per-Turn Event Example
```json
{
  "turn": 42,
  "timestamp": "2025-10-07T12:34:56.789Z",
  "agents": {
    "A": {
      "piece": "T",
      "placement": {"x": 4, "rotation": 1, "lines_cleared": 2},
      "score_delta": 300,
      "garbage_sent": 1,
      "decision_time_ms": 147,
      "timed_out": false,
      "comment": "Set up flat surface; sent Z earlier to distort opponent stack",
      "bank_view_before": {"I":12,"O":13,"T":10,"S":8,"Z":9,"J":11,"L":12}
    },
    "B": {
      "piece": "Z",
      "placement": {"x": 5, "rotation": 0, "lines_cleared": 0},
      "score_delta": 0,
      "garbage_received": 1,
      "decision_time_ms": 181,
      "timed_out": false
    }
  },
  "bank_state_after": {"I":12,"O":13,"T":10,"S":8,"Z":8,"J":11,"L":12},
  "attack_effectiveness": {
    "A": {"sent": 1, "opponent_cleared_next_turn": 0}
  }
}
```

### 7.2 File Organization
- One file per match: `logs/match_<ISO8601>.jsonl`.
- Final line: summary object `{ "summary": true, ... }`.
- Provide minimal schema validation helper (optional).

---

## 8. Visualization

### 8.1 Pygame
- Window with two boards side by side (margin ~16 px).
- Stats panel: per-agent score, lines cleared, garbage sent/received, remaining bank counts.
- Recent comment (if any) below each board (truncate).
- Optional toggle: `--show-comments` (default on) / `--no-show-comments`.

### 8.2 ASCII Mode
Example snapshot:
```
Turn 42
A Score: 1800  Lines: 8  Garbage Sent: 5
B Score: 1500  Lines: 6  Garbage Sent: 3

A Board:                 B Board:
..........               ..........
....##....               ......#...
....##....               ......#...
...T.....Z               ......#...
...T.....Z               .....##...
================  Bank: I:12 O:13 T:10 S:8 Z:8 J:11 L:12
A Comment: Setting up left well
B Comment: Trying to stabilize center
```
Cell encoding:
- Empty: `.`
- Occupied: piece letter (I,O,T,S,Z,J,L) or `#` (garbage fill).
ANSI colors optional (flag to disable for CI).

---

## 9. CLI

### 9.1 Core Arguments
```
python -m main \
  --mode {pygame,ascii} \
  --agent-a greedy \
  --agent-b aggressive \
  --bank-count 15 \
  --time-limit-ms 200 \
  --turn-interval 2.0 \
  --max-turns 2000 \
  --seed 123 \
  --log-dir logs
```

### 9.2 Additional Flags
- `--show-comments` / `--no-show-comments`
- `--replay <file>` (stretch)
- `--tournament <config.json>` (stretch)

---

## 10. Coding & Style
- Python 3.11
- All modules: SPDX header first line.
- Use `from __future__ import annotations`.
- Type hints (mypy-friendly).
- Keep functions ≤ ~80 lines; refactor larger logic.
- Avoid heavy dependencies: only `pygame` (visualization), stdlib modules (`argparse`, `json`, `time`, `dataclasses`, `typing`, `random`).
- Deterministic behavior under `--seed`.
- Clear docstrings (Google or NumPy style) for public classes/functions.

---

## 11. Licensing
Files required:
- `LICENSE-APACHE.md` (Apache License 2.0 full text)
- `LICENSE-MIT.md` (MIT License full text)
- `NOTICE` containing:
```
Copyright (c) 2025 Nikolay & Microsoft Copilot
```
README License section:
```
This project is licensed under either Apache License 2.0 or MIT License, at your option.
SPDX: Apache-2.0 OR MIT
```
All `.py` files: `# SPDX-License-Identifier: Apache-2.0 OR MIT` top line.

---

## 12. Testing (Minimum)
Add simple tests:
- `test_engine_line_clear.py`: place blocks to form full row → verify removal + downward shift.
- `test_bank.py`: drawing reduces counts; empties trigger fallback path.
- `test_agent_greedy.py`: returned placement is within bounds and valid.

---

## 13. Stretch Goals (Optional)
1. Replay system: `replay.py` reads JSONL and replays (pygame/ASCII).
2. Configurable heuristic weights (e.g. `agents_config.json`).
3. Tournament mode: batch matches, aggregated stats (win rate, avg lines, avg decision time).
4. Enhanced attack metrics (correlate sent piece with opponent surface roughness after N turns).
5. Rich SRS + T-Spin detection.
6. Lookahead / beam search AI variant.

---

## 14. Acceptance Criteria (Baseline “Done”)
- ASCII match runs start to finish (top out or max turns).
- JSONL logs created with keys: `turn`, `agents`, `bank_state_after`.
- Figure Bank decrements properly; fallback triggers when exhausted.
- Decision time limit enforcement: timeouts produce fallback + `timed_out: true`.
- `--turn-interval` produces visible pacing (e.g., ~2s delay).
- Optional comments appear in both logs and displays (if enabled).
- All source files contain SPDX header.
- README explains: concept, running modes, strategies, licensing.
- Dual license + NOTICE present.

---

## 15. Recommended Development Sequence
1. `game_engine.py`: board model, placement, line clears.
2. `bank.py`: FigureBank + unit test.
3. `ai_agent.py`: BaseAgent + Greedy skeleton (no advanced heuristics).
4. `arena.py`: core loop (ASCII logging stub).
5. `logging_utils.py`: JSONL writer.
6. `main.py`: CLI + ASCII mode integration.
7. Add Aggressive & Defensive strategies.
8. Pygame visualization.
9. README + licenses + NOTICE.
10. Stretch features (replay, tournament).

---

## 16. Guidance for GPT-5-Codex
- Generate scaffold first: empty but runnable modules + CLI that prints “skeleton running”.
- Fill functionality iteratively (avoid one giant >1000 line dump).
- Each module: top-level docstring summarizing purpose.
- Provide clear, cohesive naming (snake_case).
- No unused code; remove dead branches.
- Keep imports minimal.

---

## 17. README Content (Outline)
- Overview & motivation
- Quick start (ASCII demo)
- AI strategies summary
- Figure Bank explanation
- Example ASCII board
- CLI usage examples
- Logging format
- License (dual)
- Future enhancements

---

## 18. Performance Guidelines
- Internal decision must finish within `decision_time_limit_ms` (default 200 ms).
- Fast mode (`--turn-interval 0`, greedy vs greedy) target: ≥ 200 turns/sec on a typical modern CPU (non-binding).
- Demo mode: consistent pacing at user-defined `--turn-interval`.
- Optimization is secondary to clarity for first release.

---

## 19. Potential Future Improvements
- Full SRS rotation system.
- T-Spin detection scoring.
- Advanced heuristics (hole weighting, surface roughness).
- Multi-depth lookahead, beam search, or Monte Carlo playouts.
- Web UI (FastAPI + WebSocket).
- Live metrics dashboard.

---

## 20. Completion Checklist
Before tagging initial release:
- All acceptance criteria satisfied.
- Example log file included in `examples/`.
- README verified (copy/paste commands work).
- Licenses + NOTICE verified.
- Basic tests pass.
- No lingering TODO markers in critical paths (except in clearly marked stretch files).

(End of specification)