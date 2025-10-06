```markdown
# AI vs AI Tetris Arena with Figure Bank

## 🎮 Overview
This project implements a **Tetris-style competitive arena** where two AI agents battle each other.  
Unlike classic Tetris, the game introduces a **shared Figure Bank** mechanic:  
- Each AI draws pieces from a limited pool.  
- After placing a piece, an AI selects the next piece for its opponent.  
- As the bank depletes, attacking “smartly” becomes harder, forcing adaptive strategies.  

The result is a hybrid of **Tetris + resource management + adversarial AI combat**.

---

## ⚙️ Rules

1. **Game Board**
   - Each AI has its own 10×20 grid.  
   - Pieces fall from the top; AIs decide placement and rotation.  

2. **Figure Bank**
   - Initialized with a finite pool (e.g., 15 of each tetromino).  
   - When a piece is used, it is removed from the bank.  
   - If the bank is empty, the game falls back to a random generator.  

3. **Attacks**
   - After placing a piece, an AI chooses a figure from the bank to send to the opponent.  
   - If the chosen figure is unavailable, another must be selected.  
   - Clearing lines sends garbage lines to the opponent.  

4. **Scoring**
   - 1 line = 100 points  
   - 2 lines = 300 points  
   - 3 lines = 500 points  
   - 4 lines (Tetris) = 800 points  

5. **Victory**
   - The game ends when one board overflows.  
   - Winner = the AI with the higher score or the last survivor.  

---

## 🧩 ASCII Illustration

### Example Board
```
|          |
|     []   |
|   [][]   |
|   [][]   |
| [][][][] |
------------
```

### Example Figure Bank
```
BANK:
I: |||||||||||||
O: |||||||||||||
T: |||||||||||||
S: |||||||||||||
Z: |||||||||||||
L: |||||||||||||
J: |||||||||||||
```
(Each "|" represents one available piece.)

---

## 🤖 AI Strategies
- **Greedy**: minimize stack height.  
- **Aggressive**: maximize attacks by sending difficult pieces.  
- **Defensive**: prioritize survival and stability.  

---

## 📊 Logging
- JSON logs include:
  - Moves taken  
  - Time per decision  
  - Bank state after each turn  
  - Attack effectiveness  

---

## 🚀 How to Run
1. Clone the repository.  
2. Install dependencies:  
   ```bash
   pip install -r requirements.txt
   ```  
3. Run the game in **pygame mode**:  
   ```bash
   python main.py
   ```  
4. Run in **ASCII mode** (headless):  
   ```bash
   python main.py --ascii
   ```  

---

## 🛣️ Roadmap
- [ ] Add replay saving and playback.  
- [ ] Add configurable AI parameters.  
- [ ] Add tournament mode (multiple matches with statistics).  
- [ ] Improve visualization with animations and sound.  

---

## 📜 License
This project is licensed under a **dual license**:  
- [Apache License 2.0](LICENSE-APACHE.md)  
- [MIT License](LICENSE-MIT.md)  

You may choose either license.  

SPDX identifier:  
```
Apache-2.0 OR MIT
```

---

## ✨ Attribution
Copyright (c) 2025  
**Nikolay & Microsoft Copilot**
```

---

