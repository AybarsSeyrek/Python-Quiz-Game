# Python-Quiz-Game
# Professional Python Quiz Game
Terminal-based Python quiz game. The game lets players choose a category, answer randomly selected questions, receive a final score, review incorrect answers, and save high scores using JSON file storage. This project demonstrates core Python programming skills such as functions, lists, dictionaries, file handling, JSON, randomization, input validation, error handling, and modular project organization.

---

## Features

- Main menu system
- Player name input
- Three quiz categories:
  - Science
  - History
  - Movies
- 40 questions stored per category
- 10 random questions selected each playthrough
- Randomized answer choices every time a question appears
- Input validation for menu choices and quiz answers
- Score and percentage calculation
- Wrong-answer review after each quiz
- High-score saving using JSON
- Option to view previous high scores
- Play-again option
- Questions stored in a separate `questions.json` file
- High scores saved in `high_scores.json`
- Main game code stored in `quiz_game.py`

---

## Project Structure

```text
Python_Quiz_Game/
│
├── quiz_game.py
├── questions.json
├── high_scores.json
└── README.md
```

### `quiz_game.py`

The main Python file that contains the game logic, including the menu system, category selection, random question selection, answer checking, score calculation, wrong-answer review, and high-score saving.

### `questions.json`

Stores all quiz questions separately from the main Python code. Each category contains a larger question pool, allowing the game to randomly select questions for each playthrough.

### `high_scores.json`

Stores saved player scores. This file is created automatically after a player completes a quiz.

### `README.md`

Explains the project, features, structure, and Python concepts demonstrated.

---

## How to Run

Make sure `quiz_game.py` and `questions.json` are in the same folder.

Run the program with:

```bash
python quiz_game.py
```

or:

```bash
python3 quiz_game.py
```

---

## How the Game Works

1. The player starts at the main menu.
2. The player chooses to start the quiz, view high scores, or exit.
3. If the player starts a quiz, they enter their name.
4. The player chooses a category: Science, History, or Movies.
5. The game randomly selects 10 questions from the selected category's 40-question pool.
6. The answer choices are shuffled every time a question appears.
7. The player answers by typing A, B, C, or D.
8. The game checks whether the selected answer text matches the correct answer.
9. At the end, the game shows the score, percentage, and wrong-answer review.
10. The score is saved to `high_scores.json`.
11. The player can choose to play again or exit.

---

## Technical Concepts Demonstrated

### Functions and Modular Code Organization

The program is divided into functions such as `display_main_menu()`, `run_quiz()`, `ask_question()`, `save_high_score()`, and `view_high_scores()`.

This keeps the code organized, easier to read, and easier to update.

### Lists and Dictionaries

The quiz data uses lists and dictionaries to organize categories, questions, answer choices, and correct answers.

Each question is stored as structured data:

```json
{
    "question": "What is the chemical symbol for gold?",
    "options": ["Go", "Gd", "Au", "Ag"],
    "answer": "Au"
}
```

This demonstrates how Python data structures can be used to organize real program data.

### JSON File Handling

The project uses JSON files to store questions and high scores.

Questions are loaded from `questions.json`, and scores are saved to `high_scores.json`.

```python
with open(QUESTIONS_FILE, "r", encoding="utf-8") as file:
    return json.load(file)
```

This demonstrates reading from and writing to external files using Python's built-in `json` module.

### Separating Data from Logic

The questions are stored in `questions.json` instead of being hard-coded directly inside `quiz_game.py`.

This separates the game logic from the quiz data, making the project cleaner and easier to maintain.

### Random Question Selection

The game uses `random.sample()` to select 10 unique questions from a larger 40-question category pool.

```python
selected_questions = random.sample(question_pool, QUESTIONS_PER_GAME)
```

This ensures that each playthrough uses a different set of questions without repeating questions in the same round.

### Randomized Answer Choices

The game uses `random.shuffle()` to randomize the answer choices every time a question appears.

```python
shuffled_options = question_data["options"].copy()
random.shuffle(shuffled_options)
```

The shuffled options are then assigned to A, B, C, and D. This prevents the correct answer from always appearing in the same position.

### Mapping User Input to Answer Text

Instead of storing the correct answer as a fixed letter, the game stores the correct answer as text.

For example:

```json
{
    "question": "Which movie features the character Don Corleone?",
    "options": ["The Godfather", "Scarface", "Goodfellas", "Heat"],
    "answer": "The Godfather"
}
```

The program maps the player's letter choice to the actual answer text, then compares that selected text to the correct answer.

This allows the answer choices to be shuffled while still checking answers correctly.

### Input Validation

The game validates user input for menu choices, category selection, quiz answers, and the play-again option.

For example, quiz answers must be A, B, C, or D.

```python
if guess_letter in answer_letters:
    return selected_answer_text
```

This prevents invalid input from crashing the program or being accepted incorrectly.

### Score and Percentage Calculation

The game tracks the number of correct answers and calculates the final percentage.

```python
percentage = int((score / total_questions) * 100)
```

This demonstrates basic arithmetic, variables, and score tracking.

### Wrong-Answer Review

The program stores incorrect answers in a list of dictionaries.

```python
wrong_answers.append({
    "question": question_data["question"],
    "your_answer": selected_answer,
    "correct_answer": correct_answer
})
```

At the end of the quiz, the game displays the missed questions, the player's selected answers, and the correct answers.

This demonstrates how to collect and display structured data during program execution.

### High-Score Saving

After each quiz, the player's name, category, score, percentage, and date/time are saved to `high_scores.json`.

```python
json.dump(high_scores, file, indent=4)
```

This allows scores to stay saved even after the program closes.

### Viewing and Sorting High Scores

The game can load previous scores from `high_scores.json` and display them from highest to lowest percentage.

```python
sorted_scores = sorted(
    high_scores,
    key=lambda score_data: score_data["percentage"],
    reverse=True
)
```

This demonstrates sorting lists of dictionaries and using a lambda function.

### Error Handling

The program uses `try` and `except` blocks when reading JSON files.

```python
try:
    with open(HIGH_SCORE_FILE, "r", encoding="utf-8") as file:
        return json.load(file)
except json.JSONDecodeError:
    return []
```

This helps prevent the program from crashing if a JSON file is empty or incorrectly formatted.

### Date and Time Tracking

The game records when each quiz attempt was completed using Python's `datetime` module.

```python
datetime.now().strftime("%Y-%m-%d %H:%M:%S")
```

This adds more useful information to each saved high-score entry.

---

## Python Concepts Practiced

This project demonstrates the following Python concepts:

- Variables
- Constants
- Functions
- Lists
- Dictionaries
- Nested data structures
- Loops
- Conditional statements
- User input
- Input validation
- File handling
- JSON reading and writing
- Error handling with `try` and `except`
- Randomization with the `random` module
- Date and time with the `datetime` module
- Sorting with `sorted()`
- Lambda functions
- Separating data from program logic
- Modular project organization

---

## Standard Libraries Used

This project only uses Python standard libraries.

```python
import random
import json
import os
from datetime import datetime
```

### `random`

Used to randomly select questions and shuffle answer choices.

### `json`

Used to load questions from `questions.json` and save scores to `high_scores.json`.

### `os`

Used to check whether files exist before opening them.

### `datetime`

Used to save the date and time of each quiz attempt.

---

## What I Learned

While building this project, I practiced creating a complete terminal-based Python application with organized code and external data storage.

I learned how to structure a program using functions, store data with lists and dictionaries, load and save JSON files, validate user input, handle errors, and use randomization to make a game more replayable.

I also learned how separating the question data into `questions.json` makes the project cleaner and easier to maintain compared to keeping all questions directly inside the main Python file.
