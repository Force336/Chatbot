# importing Modules
import csv


# Importing classes
from User_Questions import UserQuestions
from User_Sentences import UserSentences

# Importing functions
from Global import sigmoid

# Importing variables
from Questions import short_term_memory_list


class SentenceCalculator:
    def __init__(self, s):
        self.user_question = None
        self.user_sentence = None

        self.sentence = s.lower()
        self.emotion_sum = 0
        self.question_sum = 0

        self.average_emotion = 0
        self.average_question = 0

        self.emotion_words_sum = 0
        self.questioning_words_sum = 0

    def split(self):
        return self.sentence.split()

    def calculator(self):
        for i in self.split():
            # read CSV file
            with open('Emotion sheet.csv', mode='r') as csv_file:
                csv_reader = csv.DictReader(csv_file)
                for row in csv_reader:

                    # emotion identifier
                    if i == row["words"]:
                        """"
                        Adds values of emotion and question 
                        to their own lists
                        """

                        if row["emotion"] != "0":
                            self.emotion_words_sum += 1
                            self.emotion_sum += float(row["emotion"])

                        if row["questioning"] != "0":
                            self.questioning_words_sum += 1
                            self.question_sum += float(row["questioning"])
                        break

            # question identifier
            if "?" in i:
                """
                If question Mark was used, the value of question increases
                And the question mark will not be taken in consideration when comparing
                """
                self.question_sum += len(self.split()) * 10
                self.sentence = self.sentence.replace("?", "")

            else:
                """"
                Checks if the entire question has already been asked
                if it is exactly the same word for word, then it is a question
                """""

                with open('Questions.csv', mode='r') as csv_file:
                    csv_reader = csv.DictReader(csv_file)
                    for row in csv_reader:
                        if row["Questions"].lower() == self.sentence.lower():
                            self.question_sum += len(self.split()) * 10
                            break

    def average_emotion_calculator(self):
        if self.emotion_words_sum != 0:
            self.average_emotion = self.emotion_sum / self.emotion_words_sum

    def average_question_calculator(self):
        try:
            self.average_question = sigmoid(self.question_sum / (len(self.sentence)))

        except ZeroDivisionError:
            self.average_question = 0.5

        print("Question average --->", self.average_question)

    def is_it_a_question(self):
        """
        Checks if the sentence is a question or not
        """
        if self.average_question >= 0.7:
            self.user_question = UserQuestions(self)
            # print("Question")
            self.user_question.update()
        else:
            self.user_sentence = UserSentences(self)
            # print("Sentence")
            self.user_sentence.update()

    def update(self):
        self.calculator()
        self.average_emotion_calculator()
        self.average_question_calculator()
        self.is_it_a_question()
        short_term_memory_list.append(self.sentence)
