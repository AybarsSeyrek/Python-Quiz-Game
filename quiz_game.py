# Main file for the quiz game.
#
# This file contains the game logic.
# The questions are stored separately in questions.json.
#
# Features:
# - Main menu
# - Categories
# - 40-question pool per category
# - 10 random questions per playthrough
# - Randomized answer choices
# - Wrong-answer review
# - High-score saving with JSON
# - Play again option

import random
import json
import os
from datetime import datetime


QUESTIONS_FILE = "questions.json"
HIGH_SCORE_FILE = "high_scores.json"
QUESTIONS_PER_GAME = 10


def load_questions():
    # This function loads the question data from questions.json.
    # Keeping questions in a separate file makes the project cleaner.
    if not os.path.exists(QUESTIONS_FILE):
        print(f"Error: {QUESTIONS_FILE} was not found.")
        print("Make sure questions.json is in the same folder as quiz_game.py.")
        return {}

    try:
        with open(QUESTIONS_FILE, "r", encoding="utf-8") as file:
            return json.load(file)

    except json.JSONDecodeError:
        print(f"Error: {QUESTIONS_FILE} has invalid JSON formatting.")
        return {}


def display_main_menu():
    # This menu makes the game feel more like a real program.
    print("=" * 50)
    print("              PROFESSIONAL QUIZ GAME")
    print("=" * 50)
    print("1. Start Quiz")
    print("2. View High Scores")
    print("3. Exit")
    print("=" * 50)


def get_menu_choice():
    # Keep asking until the user enters a valid menu choice.
    while True:
        choice = input("Choose an option: ").strip()

        if choice in ["1", "2", "3"]:
            return choice

        print("Invalid choice. Please enter 1, 2, or 3.")


def get_player_name():
    # The player's name will be saved with their score.
    while True:
        name = input("Enter your name: ").strip()

        if name:
            return name

        print("Name cannot be empty.")


def choose_category(quiz_categories):
    # Convert category names into a list so we can show them as numbered choices.
    categories = list(quiz_categories.keys())

    if not categories:
        print("No categories found.")
        return None

    print("\nChoose a category:")
    for index, category in enumerate(categories, start=1):
        print(f"{index}. {category}")

    while True:
        choice = input("Enter category number: ").strip()

        if choice.isdigit():
            choice = int(choice)

            if 1 <= choice <= len(categories):
                return categories[choice - 1]

        print("Invalid category. Please choose a valid number.")


def select_random_questions(quiz_categories, category):
    # Each category has 40 questions, but each game only asks 10.
    question_pool = quiz_categories[category]

    # This check prevents the program from crashing if a category has too few questions.
    if len(question_pool) < QUESTIONS_PER_GAME:
        print(f"Warning: {category} has fewer than {QUESTIONS_PER_GAME} questions.")
        return question_pool.copy()

    # random.sample chooses 10 different questions without repeating.
    selected_questions = random.sample(question_pool, QUESTIONS_PER_GAME)

    # This makes sure the 10 selected questions appear in random order.
    random.shuffle(selected_questions)

    return selected_questions


def ask_question(question_data, question_number):
    print("-" * 50)
    print(f"Question {question_number}: {question_data['question']}")

    # Copy the options so the original question data stays unchanged.
    shuffled_options = question_data["options"].copy()

    # This randomizes where the correct answer appears.
    # For example, the correct answer might be A one time and C another time.
    random.shuffle(shuffled_options)

    answer_letters = ["A", "B", "C", "D"]
    letter_to_option = {}

    # Attach A, B, C, and D to the shuffled answer choices.
    for index, option in enumerate(shuffled_options):
        letter = answer_letters[index]
        letter_to_option[letter] = option
        print(f"{letter}. {option}")

    # The player still answers using a letter.
    while True:
        guess_letter = input("Enter your answer (A, B, C, D): ").upper().strip()

        if guess_letter in answer_letters:
            # Convert the player's letter into the actual answer text.
            selected_answer_text = letter_to_option[guess_letter]
            return selected_answer_text

        print("Invalid answer. Please enter A, B, C, or D.")


def run_quiz(quiz_categories):
    player_name = get_player_name()
    category = choose_category(quiz_categories)

    if category is None:
        return

    questions = select_random_questions(quiz_categories, category)

    score = 0
    wrong_answers = []

    print(f"\nStarting {category} Quiz...")
    print(f"You will answer {len(questions)} random questions.")
    print("Good luck!\n")

    for question_number, question_data in enumerate(questions, start=1):
        selected_answer = ask_question(question_data, question_number)
        correct_answer = question_data["answer"]

        # Since the answer choices are randomized, we compare answer text to answer text.
        if selected_answer == correct_answer:
            score += 1
            print("Correct!\n")
        else:
            print("Incorrect!")
            print(f"The correct answer was: {correct_answer}\n")

            # Save the actual answer text for the final review.
            wrong_answers.append({
                "question": question_data["question"],
                "your_answer": selected_answer,
                "correct_answer": correct_answer
            })

    percentage = int((score / len(questions)) * 100)

    display_results(category, score, len(questions), percentage, wrong_answers)
    save_high_score(player_name, category, score, len(questions), percentage)


def display_results(category, score, total_questions, percentage, wrong_answers):
    print("=" * 50)
    print("                    RESULTS")
    print("=" * 50)
    print(f"Category: {category}")
    print(f"Score: {score}/{total_questions}")
    print(f"Percentage: {percentage}%")

    if percentage == 100:
        print("Feedback: Perfect score! Excellent work.")
    elif percentage >= 80:
        print("Feedback: Great job!")
    elif percentage >= 60:
        print("Feedback: Not bad, but you can improve.")
    else:
        print("Feedback: Keep practicing.")

    print("=" * 50)

    show_wrong_answers(wrong_answers)


def show_wrong_answers(wrong_answers):
    # If there are no wrong answers, there is nothing to review.
    if not wrong_answers:
        print("\nYou got every question correct!")
        return

    print("\nWrong Answer Review")
    print("-" * 50)

    for index, item in enumerate(wrong_answers, start=1):
        print(f"{index}. Question: {item['question']}")
        print(f"   Your answer: {item['your_answer']}")
        print(f"   Correct answer: {item['correct_answer']}")
        print()


def load_high_scores():
    # If the high-score file does not exist yet, start with an empty list.
    if not os.path.exists(HIGH_SCORE_FILE):
        return []

    try:
        with open(HIGH_SCORE_FILE, "r", encoding="utf-8") as file:
            return json.load(file)

    # If the file is empty or broken, this prevents the program from crashing.
    except json.JSONDecodeError:
        return []


def save_high_score(player_name, category, score, total_questions, percentage):
    high_scores = load_high_scores()

    new_score = {
        "name": player_name,
        "category": category,
        "score": score,
        "total_questions": total_questions,
        "percentage": percentage,
        "date_time": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }

    high_scores.append(new_score)

    with open(HIGH_SCORE_FILE, "w", encoding="utf-8") as file:
        json.dump(high_scores, file, indent=4)

    print(f"\nHigh score saved to {HIGH_SCORE_FILE}.")


def view_high_scores():
    high_scores = load_high_scores()

    if not high_scores:
        print("\nNo high scores found yet.")
        return

    print("\n" + "=" * 50)
    print("                  HIGH SCORES")
    print("=" * 50)

    # Sort scores from highest percentage to lowest percentage.
    sorted_scores = sorted(
        high_scores,
        key=lambda score_data: score_data["percentage"],
        reverse=True
    )

    for index, score_data in enumerate(sorted_scores, start=1):
        print(f"{index}. {score_data['name']}")
        print(f"   Category: {score_data['category']}")
        print(f"   Score: {score_data['score']}/{score_data['total_questions']}")
        print(f"   Percentage: {score_data['percentage']}%")
        print(f"   Date: {score_data['date_time']}")
        print("-" * 50)


def ask_play_again():
    while True:
        choice = input("\nDo you want to play again? (yes/no): ").lower().strip()

        if choice in ["yes", "y"]:
            return True
        elif choice in ["no", "n"]:
            return False

        print("Please enter yes or no.")


def main():
    # Load questions once when the program starts.
    quiz_categories = load_questions()

    if not quiz_categories:
        print("The game cannot start because no questions were loaded.")
        return

    # This loop keeps the program running until the player exits.
    while True:
        display_main_menu()
        choice = get_menu_choice()

        if choice == "1":
            run_quiz(quiz_categories)

            if not ask_play_again():
                print("\nThanks for playing!")
                break

        elif choice == "2":
            view_high_scores()

        elif choice == "3":
            print("\nGoodbye!")
            break


# This starts the game.
if __name__ == "__main__":
    main()

