
# importing modules
import csv


# importing classes
from Questions import AIQuestions, DoQuestion1, DoQuestion2, DoQuestion3, WhatQuestion, HowQuestion, WhyQuestion, WhyQuestion2, HaveYouEverQuestion, ReboundQuestion
from Sentence_Calculator import SentenceCalculator
from User_Questions import UserQuestions

# Importing functions
from Questions import verb_and_noun_object_determinate, choose_question, choose_random_question
from Global import sigmoid, question_percentage, question_match, join_string, better_questions_answers

# importing variables
from Questions import short_term_memory_list, object_verb, object_noun, recursion_fix


# ============================================ Global Variables =======================================================
""""
This 2d list will contain all the user inputted sentences
with their value of emotion and questioning
"""
user_sentences = []


# =====================================================================================================================
# ============================================ Global Functions =======================================================

# Starting function
def start():
    with open('Already Asked Question Combinations.csv', mode='w', newline='') as csv_file:
        wtr = csv.writer(csv_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        wtr.writerow(["Combinations"])

# =====================================================================================================================

start()
running = True
while running:
    """""
    This stores how many times a question has been changed due to recursion. If it increases too much, a random question
    is asked, so that no error occurs.
    1. The first number stores the current number of recursions
    2. The second number stores the maximum number of recursions
    """""
    recursion_fix = [0, 1000]

    user_input_string = str(input("User ---> "))
    user_input = SentenceCalculator(user_input_string)
    user_input.update()

    AI_question = choose_question(user_input)
    AI_question.update()
    # You can choose if deleting the object or not
    del AI_question

    # # Deleting all data in these lists
    print(short_term_memory_list, object_noun, object_verb)
    print(user_input.average_emotion)
