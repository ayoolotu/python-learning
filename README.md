# Python Learning Projects

Welcome to my **Python Learning** repository!  
This folder contains small Python scripts I created while learning **file handling**, **loops**, **functions**, and **interactive programs**.  

Each project is contained in a single `.py` file — simple and easy to run.

---

## 🧱 Files

| File | Description |
|------|-------------|
| `golf_scores.py` | Program to record and analyze golf scores |
| `movie_quiz.py` | Interactive multiple-choice movie quiz game |
| `README.md` | This file — overview of both projects |

---

## 📘 Projects Included

### 1️⃣ `golf_scores.py`
A program for tracking golf scores and analyzing performance.

**Features:**
- Prompts the user for player names and scores
- Stores scores in a list
- Calculates:
  - Best hole performance relative to par
  - List of holes where best score occurred
- Handles invalid input (non-integers, negative scores, unequal lists)

**Concepts practiced:**
- Functions and modular design
- Loops and lists
- Conditional statements
- Input validation

**Example:**

```bash
python golf_scores.py

Enter score for hole 1: 4
Enter score for hole 2: 5
Enter score for hole 3: 3

Best score: 1 under par
Scored on the following holes: [3]
```

### 2️⃣ `movie_quiz.py` 🎬

An interactive quiz that suggests movies based on your answers.

**Features:**
- Multiple-choice questions (5 total)  
- Tracks scores for 4 different movies  
- Determines recommended movie(s) or whether the program would watch them with you  
- Handles input validation and invalid choices  

**Concepts practiced:**
- Lists and loops  
- Conditionals (`if`/`else`)  
- User input validation  
- Basic scoring logic  

**Example:**

```bash
python movie_quiz.py
What is your name? Alex

Welcome to the movie quiz, Alex!
Answer the questions by typing the number of your choice.

Question 1 - When you're at a party, what are you most likely to do?
1 - Be the center of attention
2 - Stay mysterious in the corner
3 - Jump between groups of friends
4 - Keep to yourself and observe
Your choice: 2

Question 2 - Which word best describes your vibe?
1 - Bold
2 - Dark
3 - Chaotic
4 - Reflective
Your choice: 3

...

Based on your answers, I recommend you watch Everything Everywhere All At Once, Alex.
```
## 🧰 Requirements

- **Python 3.8+**
- No external libraries required

---

## ⚙️ How to Run

Run any script from your terminal or IDE:

```bash
python golf_scores.py
python movie_quiz.py
