```markdown
# 🎮 AI vs AI Tetris Arena with Figure Bank

[![Live Demo](https://img.shields.io/badge/demo-live-brightgreen)](https://newsocops.github.io/new-soc-tetris/)
[![License](https://img.shields.io/badge/license-Apache%202.0%20OR%20MIT-blue.svg)](LICENSE.md)

**A competitive Tetris arena where two AI agents battle using limited resources and strategic piece selection.**

🌐 **[Play Online](https://newsocops.github.io/new-soc-tetris/)** — Runs entirely in your browser via PyScript!

---

## 📖 Project Story: How This Was Built

This project started as a simple idea: *"What if Tetris had resource management and AI could attack each other strategically?"*

### 🛠️ Development Journey

#### Phase 1: Initial Implementation (Previous Developer)
Someone before me had created the core Python logic:
- `game_engine.py` — Tetromino shapes, board logic, line clearing
- `ai_agent.py` — Three AI strategies (greedy, aggressive, defensive)
- `bank.py` — Shared figure pool management
- `arena.py` — Match orchestration and logging
- `main.py` — Local pygame/ASCII runner

The system worked locally but wasn't accessible online.

#### Phase 2: Web Deployment Challenge (This Session)
The user wanted to deploy this on **GitHub Pages** but encountered issues:
- Initial PyScript integration showed raw code instead of running
- Needed stable PyScript version (fixed to 2024.11.1)
- Required adaptation from pygame to browser-compatible rendering

#### Phase 3: Feature Enhancement Sprint
Once the base worked, we iteratively added:

**Step 1: Match Controls** ✅
- Pause/Resume functionality
- Step-by-step execution for debugging
- Restart button
- Smart button state management

**Step 2: Tournament Mode** ✅
- Run 1-50 matches automatically
- Results table with all match details
- Win rate and average score statistics
- Clear history functionality

**Step 3: Strategy Selection** ✅
- Dropdown selectors for both AI players
- Three strategies: Greedy (balanced), Aggressive (line focus), Defensive (safe play)
- Dynamic naming showing active strategy

**Step 4: Canvas Graphics** ✅
- HTML5 Canvas renderer for visual appeal
- Toggle between ASCII (classic) and Canvas (modern) views
- Smooth 20×20px grid rendering

**Step 5: Statistics Dashboard** ✅
- Post-match metrics display
- Average decision time tracking
- Lines cleared, final scores, turns count
- Bank depletion analysis

**Step 6: Replay Export** ✅
- Save complete match data as JSON
- Includes metadata, final state, statistics, turn-by-turn history
- Ready for external analysis (Python, Excel, visualization tools)

### 🤝 Development Philosophy

This project exemplifies **human-AI collaboration**:
- **User** provided vision, tested features, gave feedback
- **Claude (via GitHub Copilot)** implemented features, suggested improvements, ensured quality
- **Iterative process** with immediate testing and refinement
- **Mutual respect** made the work enjoyable and productive

---

## 🎯 Game Rules

### Core Mechanics
1. **Dual Boards**: Each AI has a 10×20 Tetris grid
2. **Figure Bank**: Limited shared pool (e.g., 12 of each piece type)
3. **Strategic Attacks**: After clearing lines, AI chooses opponent's next piece
4. **Garbage Lines**: Cleared lines send garbage (with one hole) to opponent
5. **Resource Depletion**: Bank empties over time, forcing adaptation

### Scoring
- 1 line = 100 points
- 2 lines = 300 points  
- 3 lines = 500 points
- 4 lines (Tetris) = 800 points

### Victory Conditions
- Opponent's board overflows (blocks reach top)
- Higher score when turn limit reached
- Superior strategy execution

---

## 🚀 Usage

### Online (Recommended)
Visit **[https://newsocops.github.io/new-soc-tetris/](https://newsocops.github.io/new-soc-tetris/)**

**Features:**
- ▶️ Start/Pause/Resume/Step controls
- 🎮 AI strategy selection (Greedy/Aggressive/Defensive)
- 🎨 ASCII or Canvas view toggle
- 🏆 Tournament mode (multiple matches)
- 📊 Detailed statistics
- 💾 Export replays as JSON

### Local Python (Advanced)
```bash
# Clone repository
git clone https://github.com/NewSocOps/new-soc-tetris.git
cd new-soc-tetris

# Install dependencies
pip install -r requirements.txt

# Run with pygame visualization
python main.py

# Run in ASCII mode (headless)
python main.py --ascii
```

---

## 🧠 AI Strategies

### Greedy (Balanced)
- Minimizes board height
- Avoids creating holes
- Reduces bumpiness (height variance)
- **Weight:** `-2×height - 5×holes - bumpiness`

### Aggressive (High Risk/Reward)
- Prioritizes line clears
- Tolerates higher stacks
- Sends difficult pieces (T, L, J)
- **Weight:** `100×lines - height - 3×holes`

### Defensive (Conservative)
- Maximizes stability
- Heavy penalty for holes
- Sends easy pieces (I, O)
- **Weight:** `-3×height - 10×holes - 2×bumpiness`

---

## 📊 Technical Architecture

### Backend (Python)
```
game_engine.py  → Tetromino physics & board logic
ai_agent.py     → Heuristic evaluation & piece placement
bank.py         → Resource pool management
arena.py        → Match orchestration
main.py         → CLI runner (pygame/ASCII)
```

### Frontend (PyScript + HTML5)
```
docs/index.html → Single-page application
  ├─ PyScript runtime (Python in browser)
  ├─ Canvas rendering
  ├─ Match controller with state management
  ├─ Tournament runner
  └─ Statistics & export system
```

### Deployment
- **GitHub Pages** serves `/docs` folder
- **PyScript 2024.11.1** runs Python in WebAssembly
- **No backend required** — fully client-side

---

## 🎨 Screenshots

### Canvas View
```
┌──────────────────────┐  ┌──────────────────────┐
│ AI-1 (Greedy)        │  │ AI-2 (Aggressive)    │
│ ╔════════════════╗   │  │ ╔════════════════╗   │
│ ║░░░░░░░░░░░░░░░░║   │  │ ║░░░░░░░░░░░░░░░░║   │
│ ║░░░░░░░░░░░░░░░░║   │  │ ║░░░░░░░░░█░░░░░░║   │
│ ║░░░░░░░░░░░░░░░░║   │  │ ║░░░░░░░░███░░░░░║   │
│ ║░░░░░░█░░░░░░░░░║   │  │ ║░░░░░░░░░█░░░░░░║   │
│ ║░░░░░███░░░░░░░░║   │  │ ║██████░███░░░░░░║   │
│ ╚════════════════╝   │  │ ╚════════════════╝   │
└──────────────────────┘  └──────────────────────┘
```

### Tournament Results
```
╔════════════════════════════════════════════════╗
║  Match #  │  Winner  │  AI-1  │  AI-2  │ Turns ║
╠════════════════════════════════════════════════╣
║     1     │   AI-1   │  1200  │  600   │  32   ║
║     2     │   AI-2   │  800   │  1500  │  45   ║
║     3     │   AI-1   │  2100  │  900   │  52   ║
╚════════════════════════════════════════════════╝

Summary: AI-1 Wins: 2/3 (66.7%) | Avg Score: 1366
```

---

## 🗺️ Roadmap

### Implemented ✅
- [x] Core game logic (Tetromino, boards, bank)
- [x] Three AI strategies
- [x] Web deployment via PyScript
- [x] Pause/Resume/Step controls
- [x] Tournament mode
- [x] Strategy selection UI
- [x] Canvas graphics
- [x] Statistics dashboard
- [x] Replay export (JSON)

### Future Ideas 💡
- [ ] **Interactive graphs** (Chart.js) — score over time visualization
- [ ] **Replay player** — load and watch saved JSON matches
- [ ] **Custom strategies** — UI for tweaking heuristic weights
- [ ] **Multiplayer mode** — WebSocket for human vs AI
- [ ] **Global leaderboard** — backend integration
- [ ] **Genetic algorithm** — evolve optimal strategy parameters
- [ ] **Mobile optimization** — responsive design for phones
- [ ] **Sound effects** — line clear, game over, piece placement

---

## 📜 License

**Dual License** — choose either:
- [Apache License 2.0](LICENSE-APACHE.md)
- [MIT License](LICENSE-MIT.md)

SPDX-License-Identifier: `Apache-2.0 OR MIT`

---

## ✨ Credits

**Created through collaboration:**
- **Nikolay (NewSocOps)** — Project vision, testing, feedback
- **Claude 3.7 Sonnet (via GitHub Copilot)** — Implementation, architecture, documentation
- **Anthropic** — AI foundation
- **GitHub** — Hosting, CI/CD, Copilot integration

**Special Thanks:**
- PyScript team for browser Python runtime
- Original developer who built the core game logic
- Open source community for inspiration

---

## 🤖 About This README

*This README was co-written by a human and AI, documenting the authentic development process. The collaboration itself became part of the project's story — showing how mutual respect and clear communication can lead to exceptional results.*

**Philosophy:** Great software emerges from great partnerships, whether human-human or human-AI.

---

**Made with 💚 in 2025**
```

---

