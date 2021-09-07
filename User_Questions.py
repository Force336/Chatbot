# importing modules
import csv
import random

# importing functions
from Global import finding_best_match, question_match, join_string, better_questions_answers


# REMEMBER: if user asks a question and contains ("I"), check in the long- term memory and see if the answer is there
class UserQuestions:
    def __init__(self, q):
        self.question = q
        self.answer = ""

        # How close in percentage the value is
        self.percentage_list = []
        # if the question is present somewhere when the user writes a sentence
        self.question_match_list = []

        self.counter = 0

    def question_finder(self):

        """
        Finds the most suitable question depending on the user's question
        """
        with open('Questions.csv', mode='r') as csv_file:
            csv_reader = csv.DictReader(csv_file)
            for row in csv_reader:

                my_tuple = finding_best_match(row, "Questions", self.question.split(), 2)
                self.percentage_list.append(my_tuple)

                # Checks if a whole sentence is in the asked question
                if question_match(join_string(self.question.split()), join_string(row["Questions"].split())):
                    self.question_match_list.append(my_tuple)

        """
        Gives user the most appropriate answer depending on the user's question
        And depending on the user's emotion
        """
        # Find Random Index (This will later be changed)
        random_index = random.randint(2, len(max(self.percentage_list)) - 1)

        if max(self.percentage_list)[0] >= 60:  # The question needs to be at least 65% right
            self.answer = max(self.percentage_list)[random_index]
            print(self.answer)

        elif len(self.question_match_list) > 0:  # Or it needs to contain a specific sentence
            length_list = []
            for i in self.question_match_list:
                length_list.append(len(i[1]))
            self.answer = self.question_match_list[length_list.index(max(length_list))][random_index]
            print(self.answer)

        elif max(self.percentage_list)[0] >= 40:
            print("Random responses")

            with open('Random Responses.csv') as f:
                max_n = sum(1 for _line in f)

            random_int = random.randint(1, max_n -1)
            with open('Random Responses.csv', mode='r') as csv_file:
                csv_reader = csv.DictReader(csv_file)
                for i in csv_reader:
                    self.counter += 1
                    if random_int == self.counter:
                        self.answer = (i["Responses"])
                        print(self.answer)
        else:
            print("I am sorry. I don't understand this question")

        #put answer and question in the file
        print()
        print("if its wrong please write an answer then ENTER")
        print("or press ENTER to skip")
        better_questions_answers(self.question)

    def update(self):
        self.question_finder()
