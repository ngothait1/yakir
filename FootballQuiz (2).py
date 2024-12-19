import json
import time
import threading
import queue
import sys
from bidi.algorithm import get_display
sys.stdout.reconfigure(encoding='utf-8')


def loadQuestions():
    with open("C:\\Users\\User\\Desktop\\course\\targil\\heb_questions.json", encoding="utf-8") as questionsFile: # encoding = ensures proper handling of special characters.
        data = json.load(questionsFile) 
        return data["questions"]
    
    
def timeOut(question_num, score_queue, results):
    print("\nTime's up! Moving to the next question.")
    print("Press Enter to continue to the next question...")


def askQuestion(question, options, correct_answer, score_queue, question_num, results):
    start_time = time.time()  # Start the timer
    print("\nQuestion " + str(question_num) + ": " + get_display(question))
    for i, option in enumerate(options):
        print(str(i+1) + ". " + get_display(option))  # (i+1) It makes the number start from 1 instead of 0.
    answer = None
    timer_thread = threading.Timer(10.0, timeOut, args=(question_num, score_queue, results,))
    timer_thread.start()   
    while time.time() - start_time < 10 and answer is None:
        answer = input("Choose your answer  (1-4): ")
        if answer not in ["1", "2", "3", "4"]:
            print("Invalid choice. Please choose a valid option (1-4).")
            answer = None  # Reset answer so user can retry
    timer_thread.cancel()  # Cancel the timer once the user answered or time is up
    if answer is None:  # If no answer was given within the time limit
        score_queue.put(0)
        results.append((question_num, False))
    else:
        if int(answer) - 1 == correct_answer:
            score_queue.put(20)  # If the answer is correct, add 20 points
            results.append((question_num, True))
        else:
            score_queue.put(0)
            results.append((question_num, False))



def displayResults(results):
    print("Here are the details of your answers:")
    for question_num, correct in results:
        if correct:
            print("Question "+ str(question_num) +":" " Correct!")
        else:
            print("Question " + str(question_num) +":" " Incorrect.")


def evaluatingAnswers(questions, player_name):
    total_points = 0  #Total score
    total_questions = len(questions)  # Number of questions
    answered_correctly = 0  # Number of correct answers
    score_queue = queue.Queue()
    results = []
    for question_num, question_data in enumerate(questions, start=1):  # For each question in the questionnaire
        question = question_data["question"]
        options = question_data["options"]
        correct_answer = question_data["correct"]
        askQuestion(question, options, correct_answer, score_queue, question_num, results)
        points = score_queue.get()  # Get the score from the queue maintained by the thread
        total_points += points  # Adding the total score
        if points == 20:
            answered_correctly += 1
    score_percentage = (total_points / (total_questions * 20)) * 100  
    print ("\n" + player_name + " Your Quiz Results is: ")
    print("You answered correctly " + str(answered_correctly) + " out of " + str(total_questions) + " questions.")
    displayResults(results)
    print("Your final score is: " + str(total_points) + " points out of " + str(total_questions * 20) + " (" + str(score_percentage) + "%)")


def main():
    player_name = input("Please enter your name: ") 
    print("Welcome, " + player_name + "! Let's start the quiz.")
    questions = loadQuestions()
    evaluatingAnswers(questions, player_name)
if __name__ == "__main__":
    main()