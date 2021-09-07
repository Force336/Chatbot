# Importing modules
import random
import csv

# Importing functions
from Global import finding_best_match

class UserSentences:
    def __init__(self, s):
        self.object_sentence = s
        self.sentence = self.object_sentence.split()
        self.percentage_list = []
        self.answer = ""

        # when this value = 0 --> short sentence       when this value = 1 --> long sentence
        self.sentence_type = None

        # determines which answers the AI picks from "ChatBot Quick Responses"
        self.response_index = 0
        self.response_list = []

    def type_of_sentence(self):
        if len(self.sentence) < 15:
            self.sentence_type = 0
        else:
            self.sentence_type = 1

    def chat_bot_response(self):

        """ Tries to find the best response
        when the user inputs a sentence. If it is not found,
        it will try finding a short response
        """

        # Creates random choice to answer between index 0,1,2
        self.response_index = random.randint(0, 2)

        with open('ChatBot Responses.csv', mode='r') as csv_file:
            csv_reader = csv.DictReader(csv_file)
            for row in csv_reader:
                my_tuple = finding_best_match(row, "input", self.sentence, 1)
                self.percentage_list.append(my_tuple)

        random_index = random.randint(2, len(max(self.percentage_list)) - 1)
        print(max(self.percentage_list)[0])

        if max(self.percentage_list)[0] >= 70:  # The question needs to be at least 70% right
            self.answer = max(self.percentage_list)[random_index]
            print(self.answer)

        else:
            with open('ChatBot Quick Responses.csv', mode='r') as csv_file:
                csv_reader = csv.DictReader(csv_file)
                for row in csv_reader:
                    self.response_list.append(row)
            
            if self.sentence_type == 0:
                # Happy and short
                if self.object_sentence.average_emotion > 0.4:
                    print(self.response_list[0][str(self.response_index)])

                # Sad and short
                elif self.object_sentence.average_emotion < -0.4:
                    print(self.response_list[1][str(self.response_index)])

                # Neutral and short
                else:
                    print(self.response_list[2][str(self.response_index)])
            else:
                # Happy and long
                if self.object_sentence.average_emotion > 0.4:
                    print(self.response_list[3][str(self.response_index)])

                # Sad and long
                elif self.object_sentence.average_emotion < -0.4:
                    print(self.response_list[4][str(self.response_index)])

                # Neutral and long
                else:
                    print(self.response_list[5][str(self.response_index)])

    def update(self):
        self.type_of_sentence()
        self.chat_bot_response()
