# 🎯 AI vs AI Tetris Arena: Complete Creation Guide

**A Reverse-Engineered Prompt for Humans & AI Collaborators**

This guide documents how to recreate this project from scratch, incorporating lessons learned from the original development process. It's designed for **human-AI collaboration**, where a developer works with an AI assistant (like Claude, GPT, or Copilot) to build the system step-by-step.

---

## 📋 Prerequisites

### For Humans:
- Basic Python knowledge (classes, functions, data structures)
- Familiarity with git and GitHub
- Understanding of Tetris game mechanics
- Patience for iterative development

### For AI Assistants:
- Ability to write clean, documented Python code
- Understanding of game logic and heuristics
- Knowledge of web technologies (HTML, JavaScript, PyScript)
- Willingness to explain decisions and iterate based on feedback

---

## 🏗️ Phase 1: Core Game Logic (Python Backend)

### Step 1.1: Game Engine (`game_engine.py`)

**Objective:** Implement classic Tetris mechanics.

**Key Components:**
```python
# Tetromino shapes as 2D arrays
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
    - Store piece type and current rotation
    - Implement rotate() method (transpose + reverse)
    - Provide get_width() and get_height()

class GameBoard:
    - 10×20 grid (list of lists)
    - can_place(piece, x, y) → collision detection
    - place_piece(piece, x, y) → fix piece to grid
    - clear_lines() → remove full rows, calculate score
    - add_garbage_lines(n) → insert garbage from bottom with random holes
    - is_game_over() → check if top row has blocks
    - get_height_map() → column heights for AI heuristics
    - to_string() → ASCII representation for debugging
```

**Scoring:**
- 1 line = 100 points
- 2 lines = 300 points
- 3 lines = 500 points
- 4 lines = 800 points

**Critical Lesson:** Keep piece rotation simple. The transpose-then-reverse method works reliably. Test edge cases like rotating near walls.

---

### Step 1.2: Figure Bank (`bank.py`)

**Objective:** Manage a finite shared pool of pieces.

**Key Components:**
```python
TETROMINO_TYPES = ['I', 'O', 'T', 'S', 'Z', 'L', 'J']

class FigureBank:
    - __init__(initial_count=15) → create dict with counts
    - get_piece(piece_type) → decrement count, return success/fail
    - is_available(piece_type) → check if piece exists
    - get_available_pieces() → list of available types
    - get_random_available() → random choice from available
    - get_state() → return copy of internal state
    - to_string() → ASCII bar chart of remaining pieces
```

**Critical Lesson:** Always return copies of state to prevent external mutation. The bank is shared between both AIs, so thread-safety matters if you parallelize later.

---

### Step 1.3: AI Agent (`ai_agent.py`)

**Objective:** Implement decision-making strategies.

**Key Components:**
```python
class AIAgent:
    - __init__(name, strategy="greedy")
    - decide_placement(board, piece) → (x, y, rotations)
        * Try all rotations (0-3)
        * Try all x positions
        * Drop to lowest valid y
        * Evaluate each position
        * Return best placement
    
    - _evaluate_position(board, piece, x, y) → float
        * Create test board copy
        * Place piece temporarily
        * Calculate metrics:
            - max_height
            - bumpiness (sum of adjacent height differences)
            - holes (empty cells below filled cells)
        * Apply strategy-specific weights
    
    - choose_attack_piece(bank) → piece_type
        * Aggressive: prefer T, L, J (difficult)
        * Defensive: prefer I, O (easy)
        * Greedy: random from available

    - get_average_decision_time() → float
```

**Strategy Formulas:**
- **Greedy:** `-2×max_height - 5×holes - bumpiness`
- **Aggressive:** `100×lines_cleared - max_height - 3×holes`
- **Defensive:** `-3×max_height - 10×holes - 2×bumpiness`

**Critical Lesson:** Always work with board copies when evaluating. Test each strategy independently before combining them. Track decision times for performance analysis.

---

### Step 1.4: Arena (`arena.py`)

**Objective:** Orchestrate matches between two AIs.

**Key Components:**
```python
class MatchLog:
    - log_turn(turn, player, piece_type, placement, lines_cleared, 
               decision_time, bank_state, attack_piece)
    - log_game_over(winner, scores, lines_cleared)
    - save_to_file(filename) → JSON export

class Arena:
    - __init__(ai1, ai2, bank)
    - _get_next_piece() → from bank or fallback random
    - play_turn(ai, board, piece_type) → (lines, time, attack)
    - run_match(max_turns=1000) → winner_name
    - get_state() → current match state dict
```

**Match Flow:**
1. Initialize both boards and first pieces
2. For each turn:
   - Process garbage queue → add_garbage_lines()
   - AI decides placement → play_turn()
   - Clear lines → send garbage to opponent
   - AI chooses attack piece → update opponent's next piece
   - Check game_over conditions
3. Determine winner (survival or score)

**Critical Lesson:** Keep turn order consistent. Apply garbage BEFORE the turn starts, not after. Log everything for debugging.

---

### Step 1.5: Local Runner (`main.py`)

**Objective:** Test game logic with pygame or ASCII visualization.

**Key Components:**
```python
# pygame mode:
- Create two board surfaces side-by-side
- Display bank state as text overlay
- Show scores, current pieces, garbage queues
- Run match in real-time with configurable speed

# ASCII mode (--ascii flag):
- Print boards as text grids
- Update every N turns
- Useful for headless testing and CI/CD
```

**Critical Lesson:** Build ASCII mode first for rapid testing. pygame comes later for polish. Always add command-line arguments for flexibility.

---

## 🌐 Phase 2: Web Deployment (GitHub Pages)

### Step 2.1: Initial PyScript Setup

**⚠️ Common Pitfall:** Using `https://pyscript.net/latest/` causes instability.

**Correct Approach:**
```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8" />
    <title>AI vs AI Tetris (PyScript)</title>
    <!-- ✅ Use specific stable version -->
    <link rel="stylesheet" href="https://pyscript.net/releases/2024.11.1/core.css" />
    <script type="module" src="https://pyscript.net/releases/2024.11.1/core.js"></script>
</head>
<body>
    <py-config>
        packages = []
    </py-config>
    
    <py-script>
        # Your Python code here (inline or import)
    </py-script>
</body>
</html>
```

**Critical Lesson:** Pin PyScript version immediately. The `/latest/` endpoint may break unexpectedly. Check [PyScript releases](https://github.com/pyscript/pyscript/releases) for stable versions.

---

### Step 2.2: Porting Python to Browser

**Challenges:**
1. No pygame in browser
2. No file system access
3. Different event loop (asyncio)

**Solutions:**

**For Rendering:**
```python
# ASCII Mode (simplest)
def board_text(board: GameBoard) -> str:
    return board.to_string()

document.getElementById("board1").textContent = board_text(board1)

# Canvas Mode (prettier)
def draw_board_canvas(ctx, board: GameBoard):
    cell_size = 20
    for y in range(board.height):
        for x in range(board.width):
            if board.grid[y][x]:
                ctx.fillStyle = "#39ff14"
                ctx.fillRect(x * cell_size, y * cell_size, cell_size, cell_size)
```

**For Event Handling:**
```python
from js import document
from pyodide.ffi import create_proxy

def start_match(event):
    asyncio.ensure_future(run_match_async())

start_handler = create_proxy(start_match)
document.getElementById("start-btn").addEventListener("click", start_handler)
```

**For Async Execution:**
```python
async def run_match_async():
    for turn in range(max_turns):
        state = arena.step()
        update_ui()
        if state["finished"]:
            break
        await asyncio.sleep(delay)  # ← Keeps UI responsive
```

**Critical Lesson:** Start with ASCII mode in browser. Add Canvas later. Test PyScript locally with `python -m http.server` before deploying.

---

### Step 2.3: GitHub Pages Configuration

**Repository Settings:**
1. Go to **Settings** → **Pages**
2. Source: **Deploy from a branch**
3. Branch: `main`, Folder: `/docs`
4. Save and wait 1-2 minutes for deployment

**File Structure:**
```
repo/
├── docs/
│   └── index.html          ← Your PyScript app
├── game_engine.py          ← Python modules (for local testing)
├── ai_agent.py
├── bank.py
├── arena.py
├── main.py
├── requirements.txt
└── README.md
```

**Critical Lesson:** GitHub Pages caches aggressively. After pushing, wait 2-3 minutes and do a hard refresh (Ctrl+F5). If still not working, check browser DevTools console for errors.

---

## 🎨 Phase 3: Feature Enhancements (Iterative)

### Enhancement 1: Match Controls

**Features to Add:**
- ⏸️ Pause/Resume
- ⏭️ Step (single turn execution)
- 🔄 Restart
- 🎚️ Speed slider

**Implementation Pattern:**
```python
class MatchController:
    is_running = False
    is_paused = False
    
    def update_buttons(self, running, paused, finished):
        # Enable/disable buttons based on state
        start_btn.disabled = running
        pause_btn.disabled = not running or paused or finished
        resume_btn.disabled = not paused or finished
```

**Critical Lesson:** State management is crucial. One button's state affects others. Draw a state machine diagram before coding.

---

### Enhancement 2: Tournament Mode

**Features to Add:**
- Run N matches automatically
- Collect results in table
- Show win rate and averages

**Implementation Pattern:**
```python
async def run_tournament(num_matches):
    results = []
    for i in range(num_matches):
        arena = Arena(ai1, ai2, bank)
        winner = await run_match_fast(arena)  # No delays
        results.append({
            "match": i+1,
            "winner": winner,
            "scores": arena.get_scores(),
            "turns": arena.turn
        })
        update_progress(i+1, num_matches)
    
    display_results_table(results)
    calculate_statistics(results)
```

**Critical Lesson:** Use minimal delays in tournament mode (0.001s) for speed. Only update UI every few turns to prevent slowdown.

---

### Enhancement 3: Strategy Selection

**Features to Add:**
- Dropdown for AI-1 strategy
- Dropdown for AI-2 strategy
- Dynamic AI naming

**Implementation Pattern:**
```html
<select id="ai1-strategy">
    <option value="greedy">Greedy (Balanced)</option>
    <option value="aggressive">Aggressive (Line Clears)</option>
    <option value="defensive">Defensive (Safe Play)</option>
</select>
```

```python
ai1_strategy = document.getElementById("ai1-strategy").value
ai1 = AIAgent(f"AI-1 ({ai1_strategy.capitalize()})", strategy=ai1_strategy)
```

**Critical Lesson:** Make UI changes affect both single matches AND tournaments. Users expect consistency.

---

### Enhancement 4: Visualization Toggle

**Features to Add:**
- Switch between ASCII and Canvas views
- Preserve match state during toggle

**Implementation Pattern:**
```python
use_canvas_view = False

def switch_to_canvas():
    global use_canvas_view
    use_canvas_view = True
    canvas1.style.display = "block"
    board1_pre.style.display = "none"
    if controller.arena:
        controller.update_ui()  # Redraw in new mode
```

**Critical Lesson:** Canvas is prettier but harder to debug. Keep ASCII mode for development. Let users choose based on preference.

---

### Enhancement 5: Statistics Dashboard

**Features to Add:**
- Post-match metrics
- Average decision times
- Lines cleared breakdown
- Bank depletion analysis

**Implementation Pattern:**
```python
def display_stats(arena):
    stats = {
        "ai1_score": arena.board1.score,
        "ai2_score": arena.board2.score,
        "ai1_avg_time": arena.ai1.get_average_decision_time() * 1000,
        "turns": arena.turn,
        "bank_remaining": arena.bank.get_total_remaining()
    }
    
    html = generate_stat_cards(stats)
    document.getElementById("stats").innerHTML = html
```

**Critical Lesson:** Collect statistics incrementally during match, not just at the end. This allows real-time graphs later.

---

### Enhancement 6: Replay Export

**Features to Add:**
- Save match as JSON
- Include metadata, history, statistics
- Download as file

**Implementation Pattern:**
```python
def export_replay():
    from js import JSON, Blob, URL, document
    
    data = {
        "version": "1.0",
        "timestamp": Date.new().toISOString(),
        "match_info": {...},
        "final_state": {...},
        "history": controller.match_stats
    }
    
    json_str = JSON.stringify(data, None, 2)
    blob = Blob.new([json_str], {"type": "application/json"})
    url = URL.createObjectURL(blob)
    
    link = document.createElement("a")
    link.href = url
    link.download = f"replay_{timestamp}.json"
    link.click()
    URL.revokeObjectURL(url)
```

**Critical Lesson:** Design JSON format for forward compatibility. Include version field. Future you will thank you when adding new metrics.

---

## 📚 Development Best Practices

### For Humans:

1. **Test Early, Test Often**
   - Write ASCII tests before pygame
   - Test each AI strategy independently
   - Verify edge cases (empty bank, board overflow, tie scores)

2. **Iterate in Small Steps**
   - Don't try to build everything at once
   - Add one feature, test it, commit it
   - Keep commits atomic and well-described

3. **Communicate Clearly with AI**
   - Describe what you want and why
   - Provide context about previous attempts
   - Ask for explanations of complex code
   - Give feedback on what works/doesn't

4. **Version Control Discipline**
   - Use feature branches for experiments
   - Merge to main only when stable
   - Tag releases with semantic versioning
   - Write meaningful commit messages

### For AI Assistants:

1. **Explain Your Decisions**
   - Don't just provide code—describe the approach
   - Mention trade-offs and alternatives
   - Warn about potential issues
   - Suggest testing strategies

2. **Write Self-Documenting Code**
   - Use clear variable names
   - Add docstrings to functions/classes
   - Include inline comments for complex logic
   - Provide type hints where helpful

3. **Anticipate Questions**
   - Explain non-obvious design choices
   - Reference best practices
   - Link to documentation when relevant
   - Offer to clarify unclear parts

4. **Respect Human Preferences**
   - Follow their coding style
   - Honor their architectural decisions
   - Adapt complexity to their skill level
   - Be patient with iterations

---

## 🐛 Common Pitfalls & Solutions

### Pitfall 1: PyScript Shows Raw Code
**Symptom:** Browser displays Python code as text instead of executing it.

**Causes:**
- PyScript JS/CSS didn't load (network error, ad blocker)
- Using unstable `/latest/` endpoint
- Missing or malformed `<py-config>`

**Solution:**
- Pin specific PyScript version (2024.11.1 or newer stable)
- Check browser DevTools console for errors
- Test in incognito mode to rule out extensions
- Use `python -m http.server` locally before deploying

---

### Pitfall 2: AI Makes Invalid Moves
**Symptom:** Pieces placed outside board, overlapping existing blocks, or causing crashes.

**Causes:**
- `can_place()` logic has bugs
- AI tries negative coordinates
- Rotation increases piece dimensions beyond board width

**Solution:**
- Add boundary checks in `can_place()`: `0 <= x < width` AND `0 <= y < height`
- Log every placement attempt to find patterns
- Add assertion: `assert board.can_place(piece, x, y)` before `place_piece()`

---

### Pitfall 3: Bank Runs Out Too Fast
**Symptom:** Bank depletes in 20-30 turns, game becomes random Tetris.

**Causes:**
- Initial count too low (e.g., 5 of each)
- Both AIs aggressively attacking with rare pieces
- No fallback to random generator

**Solution:**
- Use 12-15 initial pieces per type
- Implement fallback: `if bank.is_empty(): piece = random.choice(TYPES)`
- Balance AI strategies: not all should be "aggressive"

---

### Pitfall 4: GitHub Pages Not Updating
**Symptom:** Push to main, but website shows old version.

**Causes:**
- GitHub Pages build delay (1-3 minutes)
- Browser cache
- Changes pushed to wrong branch

**Solution:**
- Wait 2-3 minutes after push
- Hard refresh: Ctrl+F5 (Windows) / Cmd+Shift+R (Mac)
- Check GitHub Actions tab for build status
- Verify Settings → Pages shows correct branch/folder

---

### Pitfall 5: Decision Times Too Slow
**Symptom:** AI takes 2-5 seconds per move, match feels sluggish.

**Causes:**
- Evaluating too many positions (10 width × 4 rotations = 40 positions)
- Creating full board copies for each evaluation
- Not optimizing heuristic calculations

**Solution:**
- Use list comprehensions instead of loops
- Cache height calculations
- Profile code: `import cProfile`
- Consider reducing search depth for weaker devices

---

## 📜 Licensing Strategy

**Recommendation: Dual License (Apache-2.0 OR MIT)**

### Why Dual License?

1. **Apache 2.0** → Patent protection, corporate-friendly
2. **MIT** → Maximum simplicity, permissive
3. **User's Choice** → Pick whichever fits their needs

### Required Files:

```
LICENSE.md              ← Summary with SPDX identifier
LICENSE-APACHE.md       ← Full Apache 2.0 text
LICENSE-MIT.md          ← Full MIT text
NOTICE                  ← Attribution and copyright
```

### SPDX Headers in Code:

```python
# SPDX-License-Identifier: Apache-2.0 OR MIT
# Copyright (c) 2025 Your Name & AI Assistant

"""
Module description here.
"""
```

### README Section:

```markdown
## 📜 License

This project is dual-licensed under:
- [Apache License 2.0](LICENSE-APACHE.md)
- [MIT License](LICENSE-MIT.md)

You may choose either license at your option.

SPDX-License-Identifier: `Apache-2.0 OR MIT`
```

**Critical Lesson:** Add licensing early in the project. Retrofitting is tedious and error-prone.

---

## 🎯 Final Recommendations

### Start Simple, Iterate Smartly

**Week 1:** Core game logic (game_engine, bank, ai_agent, arena)
- Focus on correctness, not performance
- Write extensive tests
- Use ASCII visualization only

**Week 2:** Local visualization (main.py with pygame)
- Make it playable and debuggable
- Add command-line options
- Profile AI performance

**Week 3:** Web deployment (PyScript + GitHub Pages)
- Port to browser-compatible code
- Start with ASCII mode
- Fix PyScript issues

**Week 4:** Feature enhancements (controls, tournament, stats, export)
- Add one feature at a time
- Test each thoroughly
- Collect user feedback

### Collaboration Tips

**Human-to-AI:**
- "I want to add pause functionality. How should we structure the state management?"
- "The AI is making invalid moves. Can you help me debug the placement logic?"
- "Explain the trade-offs between Canvas and ASCII rendering."

**AI-to-Human:**
- "I've implemented the pause feature. Here's how the state machine works: [diagram]. Would you like me to add step-through debugging as well?"
- "I found the bug in `can_place()`. The issue is on line 47 where we're not checking the upper boundary. Here's the fix with tests."
- "For rendering, Canvas is smoother but harder to debug. I recommend keeping both modes. Here's a toggle implementation."

### Success Metrics

**Technical:**
- [ ] AI makes 0 invalid moves in 1000-turn matches
- [ ] Average decision time < 100ms per move
- [ ] Bank lasts 150+ turns before depletion
- [ ] GitHub Pages loads in < 5 seconds
- [ ] All tests pass (unit + integration)

**User Experience:**
- [ ] Match is visually understandable
- [ ] Controls are intuitive
- [ ] Statistics are meaningful
- [ ] Export format is documented

**Collaboration:**
- [ ] Human understands all code
- [ ] AI explains design choices
- [ ] Iterations feel productive
- [ ] Both parties learn something new

---

## 🌟 Philosophical Closing

This guide represents more than just technical instructions—it documents a **partnership model** for human-AI software development.

**For Humans:**
Your role is to provide vision, judgment, and context. You decide what "good" looks like. You test in real-world conditions. You give feedback that only lived experience can provide.

**For AI:**
Your role is to implement efficiently, suggest improvements, catch errors, and explain clearly. You bring pattern recognition from thousands of codebases. You tireless iterate until it works.

**Together:**
You create something neither could build alone—a system that's technically sound AND human-centered. The code is a record of your conversations. The commits tell the story of your collaboration.

When you disagree, you discuss. When you're stuck, you experiment. When you succeed, you both learn.

**That's the future of software development.**

---

## 📞 Support & Community

If you're recreating this project and encounter issues:

1. **Check this guide first** — most problems are covered
2. **Review the commit history** — see how we solved similar issues
3. **Read the inline comments** — code documents itself
4. **Test incrementally** — don't build everything at once
5. **Ask specific questions** — provide context and error messages

**Remember:** Every expert was once a beginner. Every complex system started simple. Every bug has a solution. Every collaboration requires patience.

Good luck, and happy building! 🚀

---

**Document Version:** 1.0  
**Last Updated:** 2025-10-08  
**Authors:** Nikolay (Human) & Claude Sonnet 4.5 (AI)  
**License:** Apache-2.0 OR MIT
