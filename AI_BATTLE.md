# ⚔️ AI BATTLE: Inside the Minds of Tetris Warriors

## 🧠 How Our AI Agents Think

This project features **three distinct AI strategies** that compete in Tetris matches. Each agent evaluates the game board using mathematical heuristics and makes decisions in real-time without look-ahead search trees. Here's what happens inside their "minds":

---

## 🎯 The Decision-Making Process

Every time a Tetromino spawns, the AI agent:

1. **Generates all possible placements** (rotations × horizontal positions)
2. **Evaluates each placement** using its strategy formula
3. **Selects the move with the best score**
4. **Executes immediately** (no planning ahead)

This is a **greedy one-step algorithm** — fast, efficient, and surprisingly effective!

---

## 🤖 Meet the Three Warriors

### 1️⃣ **GREEDY Strategy** — *The Balanced Tactician*

**Philosophy**: Minimize holes, keep the board low, maximize line clears

**Evaluation Formula**:
```python
score = -4.0 × aggregate_height 
        -7.0 × holes 
        -3.0 × bumpiness 
        +2.0 × lines_cleared
```

**What it means**:
- **Aggregate Height** (`-4.0`): Sum of column heights → punishes tall stacks
- **Holes** (`-7.0`): Empty cells with blocks above → heavily penalized (hardest to fix)
- **Bumpiness** (`-3.0`): Height differences between adjacent columns → prefers smooth surface
- **Lines Cleared** (`+2.0`): Reward for completing lines → encourages efficiency

**Personality**: Conservative and methodical. Avoids risky moves. Good at surviving long matches.

---

### 2️⃣ **AGGRESSIVE Strategy** — *The Reckless Attacker*

**Philosophy**: Build high, attack with garbage lines, ignore surface smoothness

**Evaluation Formula**:
```python
score = +3.0 × aggregate_height 
        -5.0 × holes 
        +0.5 × bumpiness 
        +5.0 × lines_cleared
```

**What it means**:
- **Aggregate Height** (`+3.0`): *Bonus* for tall stacks → deliberately builds high
- **Holes** (`-5.0`): Still avoids holes (but less paranoid than Greedy)
- **Bumpiness** (`+0.5`): *Encourages* uneven surface → chaotic gameplay
- **Lines Cleared** (`+5.0`): Massively rewards clears → hyperaggressive line hunting

**Personality**: Chaotic and offensive. Tries to overwhelm opponents with garbage. High risk, high reward.

---

### 3️⃣ **DEFENSIVE Strategy** — *The Paranoid Survivor*

**Philosophy**: Obsessively avoid holes, keep a perfectly flat surface, play it safe

**Evaluation Formula**:
```python
score = -3.0 × aggregate_height 
        -10.0 × holes 
        -6.0 × bumpiness 
        +1.5 × lines_cleared
```

**What it means**:
- **Aggregate Height** (`-3.0`): Moderate penalty for height → cautious but not extreme
- **Holes** (`-10.0`): *Paranoid* about holes → avoids them at all costs
- **Bumpiness** (`-6.0`): Extremely values smooth surface → near-flat board ideal
- **Lines Cleared** (`+1.5`): Small reward for clears → doesn't chase them recklessly

**Personality**: Defensive and perfectionistic. Sacrifices offense for safety. Hard to kill but slow to attack.

---

## 📊 Key Metrics Explained

### **Aggregate Height**
```
Sum of all column heights
Example: [3, 5, 4, 6, 2, 4, 3, 5, 4, 3] → 39
```
- Low value = flat, safe board
- High value = dangerous, close to game over

### **Holes**
```
Empty cells with at least one filled cell above them
Example:
  ████
  ██░█  ← This empty cell is a HOLE
  ████
```
- Holes are **deadly** — impossible to clear without completing surrounding lines
- Different strategies weigh this differently (-5.0 to -10.0)

### **Bumpiness**
```
Sum of absolute height differences between adjacent columns
Example: [3, 5, 4] → |3-5| + |5-4| = 2 + 1 = 3
```
- Low bumpiness = smooth surface (easier to place pieces)
- High bumpiness = jagged surface (limits placement options)

### **Lines Cleared**
```
Number of complete horizontal lines in this placement
Values: 0, 1, 2, 3, or 4 (Tetris!)
```
- Main offensive mechanic: clears send garbage to opponent
- Some strategies chase this aggressively (+5.0), others conservatively (+1.5)

---

## ⚖️ Strategy Comparison Table

| Metric           | Greedy | Aggressive | Defensive |
|------------------|--------|------------|-----------|
| Height Weight    | `-4.0` | **`+3.0`** | `-3.0`    |
| Holes Weight     | `-7.0` | `-5.0`     | **`-10.0`** |
| Bumpiness Weight | `-3.0` | **`+0.5`** | `-6.0`    |
| Clears Weight    | `+2.0` | **`+5.0`** | `+1.5`    |
| **Style**        | Balanced | Chaotic | Conservative |
| **Risk Level**   | Medium | High | Low |
| **Playstyle**    | Versatile | Offensive | Turtle |

---

## 🎮 How They Compete

### **Greedy vs Aggressive**
- Greedy plays safe and waits for Aggressive to make mistakes
- Aggressive tries to overwhelm with garbage lines
- **Winner**: Depends on luck and board state — evenly matched!

### **Greedy vs Defensive**
- Both play cautiously, matches last LONG
- Greedy is slightly more aggressive with clears
- **Winner**: Slight edge to Greedy due to balanced approach

### **Aggressive vs Defensive**
- Fire vs Ice: total opposite philosophies
- Aggressive builds high and attacks; Defensive turtles and survives
- **Winner**: Aggressive usually wins by forcing Defensive into impossible situations

---

## 🔬 Technical Implementation

### Code Structure
```python
class AIAgent:
    def choose_action(self, piece, board, bank):
        best_score = float('-inf')
        best_move = None
        
        for rotation in range(4):  # Try all rotations
            for x in range(board.width):  # Try all positions
                if self.is_valid_placement(piece, rotation, x, board):
                    # Simulate placement
                    temp_board = board.clone()
                    temp_board.place_piece(piece, rotation, x)
                    
                    # Evaluate using strategy formula
                    score = self.evaluate_board(temp_board)
                    
                    if score > best_score:
                        best_score = score
                        best_move = (rotation, x)
        
        return best_move
```

### The Magic Formula
```python
def evaluate_board(self, board):
    height = self.calculate_aggregate_height(board)
    holes = self.count_holes(board)
    bumpiness = self.calculate_bumpiness(board)
    lines = self.count_completed_lines(board)
    
    # Apply strategy-specific weights
    score = (self.height_weight * height +
             self.holes_weight * holes +
             self.bumpiness_weight * bumpiness +
             self.lines_weight * lines)
    
    return score
```

---

## 🧪 Experiment: Create Your Own Strategy!

Want to design your own AI warrior? Try these weights:

### **"Suicide Bomber"**
```python
height_weight = +10.0   # Build as high as possible
holes_weight = +2.0     # Holes? Who cares!
bumpiness_weight = +5.0 # Maximum chaos
lines_weight = +10.0    # Clear lines at any cost
```
*Will self-destruct quickly but might take opponent down too!*

### **"Perfect Flat"**
```python
height_weight = -5.0    # Stay low
holes_weight = -15.0    # Zero tolerance for holes
bumpiness_weight = -10.0 # Obsessive about smoothness
lines_weight = +0.5     # Barely cares about clears
```
*Will maintain a beautiful flat board... until pieces run out!*

### **"Line Hunter"**
```python
height_weight = -2.0    # Some caution
holes_weight = -8.0     # Avoid holes
bumpiness_weight = -4.0 # Keep it reasonable
lines_weight = +15.0    # MASSIVE reward for clears
```
*Will chase Tetrises relentlessly!*

---

## 🏆 Tournament Results Insights

After running hundreds of matches, we've observed:

1. **No Perfect Strategy**: Each has strengths and weaknesses
2. **Context Matters**: Figure bank composition heavily influences outcomes
3. **Luck Factor**: Sometimes a bad piece sequence dooms even the best AI
4. **Emergent Behavior**: Strategies develop "personalities" over many matches

---

## 🎨 Why This Matters

This project demonstrates:
- **Heuristic AI**: Complex behavior from simple rules
- **Multi-agent Systems**: How different approaches compete
- **Emergent Complexity**: Simple formulas → sophisticated gameplay
- **Transparency**: Every decision is explainable (no black-box neural nets)

Our AIs don't "learn" in the machine learning sense — they're **hard-coded strategists**. Yet they produce fascinating, unpredictable matches that feel almost human!

---

## 🔮 Future Possibilities

Want to enhance the AI? Consider:

- **Look-ahead search**: Evaluate 2-3 moves ahead (computationally expensive)
- **Genetic algorithms**: Evolve optimal weights through tournaments
- **Opponent modeling**: Adapt strategy based on enemy behavior
- **Figure bank awareness**: Choose moves based on upcoming piece types
- **Meta-strategies**: Switch tactics mid-game based on board state

---

## 🤝 Contributing

Found an unbeatable weight configuration? Want to implement a new evaluation metric? Pull requests welcome!

**Try This Challenge**: Can you create a strategy that beats all three existing ones in a round-robin tournament?

---

## 📚 Learn More

- **Game Engine**: See `game_engine.py` for core Tetris logic
- **AI Implementation**: See `ai_agent.py` for strategy code
- **Arena System**: See `arena.py` for match management
- **Figure Bank**: See `bank.py` for piece distribution

---

## 🎯 The Ultimate Question

**Which strategy is "best"?**

After thousands of simulated matches, the answer is: **It depends!**

- Against aggressive opponents → Defensive excels
- Against defensive opponents → Aggressive wins
- In varied conditions → Greedy stays consistent

Just like rock-paper-scissors, there's no universal champion. And that's what makes it fun! 🎮

---

*Built with ❤️ by humans and AI working together*  
*Deployed at: https://newsocops.github.io/new-soc-tetris/*

