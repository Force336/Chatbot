# ------------------------------------------------------- AI Questions ----------------------------------------------------------------

# Importing Modules
from abc import ABC, abstractmethod
import csv
import random


# Importing Classes
from User_Questions import UserQuestions

# Importing functions
from Global import join_string, stop_future_unwanted_q, better_combination_q, stop_repeated_q, verb_in_gerund, remove_spaces_list



# Variables

# This list(queue) will contain all of the "objects (nouns) or verbs" or  the user has been talking about in the conversation
# there should be a function that takes each verb and noun from the user_sentence and add it to the queue
# Also, if there's a word that the computer doesn't know from the user's answer, it should be added
# with the level of emotion through the user's description
short_term_memory_list = []
object_noun = []
object_verb = []

# Whenever too many questions are wrong and all of them have already been asked, the two values will be equal to each other
recursion_fix = [0, 1000]


#--------------- Functions ---------------

# This determines whether a word from a user_input is an object_noun or object_verb
def verb_and_noun_object_determinate():
    with open('Emotion sheet.csv', mode='r') as csv_file:
        csv_reader = csv.DictReader(csv_file)
        for row in csv_reader:
            if row["WordType"] == "2" and row["words"] in short_term_memory_list[-1] and row["Conversation"] == "1":
                if row["words"] not in object_verb:
                    object_verb.append(row["words"])
            elif row["WordType"] == "3" and row["words"] in short_term_memory_list[-1] and row["Conversation"] == "1":
                if row["words"] not in object_noun:
                    object_noun.append(row["words"])


# This function will determine which question the AI will use next
def choose_question(input):

    # The vaue x will become the object of one of the questions
    x = 0
    # Choosing topic questions
    verb_and_noun_object_determinate()
    # This integer determines if the question asked is stored in "Questions" or is created by the AI
    saved_or_created = random.randint(1,10)

    if (len(object_verb) != 0 or len(object_noun) != 0) and recursion_fix[0] < recursion_fix[1]:
        if saved_or_created <= 6:
            x = SavedQuestion(input)
        else:
            if len(object_verb) != 0 and len(object_noun) != 0:
                x = choose_random_question(input)

            elif len(object_verb) != 0 and len(object_noun) == 0:
                number = random.randint(1, 3)
                if number == 1:
                    x = DoQuestion1(input)
                elif number == 2:
                    x = WhatQuestion(input)
                elif number == 3:
                    x = WhyQuestion(input)

            # elif object_verb is None and object_noun is not None:
            else:
                x = DoQuestion2(input)

    # Choosing random questions
    else:
        if recursion_fix[0] == recursion_fix[1]:
            object_noun.clear(), object_verb.clear()
        x = choose_random_question(input)

    # Creates a Rebound question and it checks if it's there or not
    if type(input.user_question) is UserQuestions:
        y = ReboundQuestion(input)
        y.create_question()

        if type(y.rebound_string) != bool:
            x = y

    return x


# This function will create a random question
def choose_random_question(input):
    number = random.randint(1, 12)
    if number == 1:
        x = DoQuestion1(input)
    elif number == 2:
        x = DoQuestion2(input)
    elif number == 3:
        x = DoQuestion3(input)
    elif number == 4:
        x = WhatQuestion(input)
    elif number == 5:
        x = HowQuestion(input)
    elif number == 6:
        x = WhyQuestion(input)
    elif number == 7:
        x = WhyQuestion2(input)
    elif number == 8:
        x = HaveYouEverQuestion(input)
    else:
        x = SavedQuestion(input)
        
    return x
# -----------------------------------------


class AIQuestions(ABC):
    @abstractmethod
    def __init__(self, s):
        self.final_string = ""
        self.unwanted_combination_list = []
        self.better_combination_list = []
        self.already_asked_questions = []
        self.verb_list = []
        self.random_verb = 0
        self.noun_list = []
        self.random_noun = 0

        self.user_input = s

    @abstractmethod
    def create_random_question(self):
        """"
        This tries to find all of the verbs, nouns, adjectvives and chooses
        a random one. This happens if the user's answer didn't have
        any objects it was talking about, the AI will try to find a
        new topic to talk about
        """

        stop_future_unwanted_q(self.unwanted_combination_list)
        better_combination_q(self.better_combination_list)
        stop_repeated_q(self.already_asked_questions)

        with open('Emotion sheet.csv', mode='r') as csv_file:
            csv_reader = csv.DictReader(csv_file)
            for row in csv_reader:
                if row["WordType"] == "2":
                    self.verb_list.append(str(row["words"]))
                elif row["WordType"] == "3":
                    self.noun_list.append(str(row["words"]))

        self.random_verb = random.randint(0, len(self.verb_list) - 1)
        self.random_noun = random.randint(0, len(self.noun_list) - 1)

    @abstractmethod
    def create_topic_question(self):
        """"
        This tries to create a question that is related to a topic the user
        has decided to talk about.
        """
        stop_future_unwanted_q(self.unwanted_combination_list)
        better_combination_q(self.better_combination_list)
        stop_repeated_q(self.already_asked_questions)

        with open('Emotion sheet.csv', mode='r') as csv_file:
            csv_reader = csv.DictReader(csv_file)
            for row in csv_reader:
                if row["WordType"] == "2" and row["words"] in object_verb:
                    self.verb_list.append(str(row["words"]))
                elif row["WordType"] == "3" and row["words"] in object_noun:
                    self.noun_list.append(str(row["words"]))

            if len(object_verb) != 0:
                self.random_verb = random.randint(0, len(self.verb_list) - 1)
            if len(object_noun) != 0:
                self.random_noun = random.randint(0, len(self.noun_list) - 1)

    @abstractmethod
    def update(self):
        # Instead of having a random question there should be a function that determines which of the two type of
        # questions is more appropriate depending on the short_term_list being empty or not

        if (len(object_verb) != 0 or len(object_noun) != 0) and (recursion_fix[0] < recursion_fix[1]):
            self.create_topic_question()
        else:
            self.create_random_question()
            print("random")

        self.final_string = join_string(self.final_string)


        # Completely wrong combinations handling
        if ((self.final_string in self.unwanted_combination_list) or (
                self.final_string in self.already_asked_questions)) and (recursion_fix[0] < recursion_fix[1]):  # and question is random

            recursion_fix[0] += 1
            new = choose_question(self.user_input)
            new.update()

        else:

            # If the AI can't find a good question that HASN'T BEEN PREVIOUSLY ASKED, it will ask a previously asked question
            if recursion_fix[0] == recursion_fix[1]:
                if len(self.already_asked_questions) != 0:
                    random_index = random.randint(0, len(self.already_asked_questions))
                    self.final_string = self.already_asked_questions[random_index]
                else:
                    self.final_string = "Great!"


            # Semi-Wrong combinations handling
            self.already_asked_questions.append(self.final_string)

            for i in self.better_combination_list:
                if self.final_string == i[0]:
                    self.final_string = (i[1], "?")
                    self.final_string = join_string(self.final_string)
                    break

            # Right combination handling
            print(self.final_string)

            if len(object_verb) != 0:
                object_verb.pop(self.random_verb)
            if len(object_noun) != 0:
                object_noun.pop(self.random_noun)

            self.remove_unwanted_combinations()

    def remove_unwanted_combinations(self):
        print("(if you don't like this combination write NO)")
        print("(if the combination makes sense but is badly written then write it)")
        print("(if you like it, press ENTER)")
        answer = str(input()).lower()

        # Wrong combinations
        if answer == "no":
            with open('Wrong Questions Combinations.csv', mode='a', newline='') as csv_file:
                wtr = csv.writer(csv_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
                wtr.writerow([self.final_string])

        if answer == "":
            # Already asked questions
            with open('Already Asked Question Combinations.csv', mode='a', newline='') as csv_file:
                wtr = csv.writer(csv_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
                wtr.writerow([self.already_asked_questions[- 1]])

        # Semi-Wrong Combinations
        elif answer != "" and answer != "no":
            with open('Better Question Combinations.csv', mode='a', newline='') as csv_file:
                wtr = csv.writer(csv_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
                wtr.writerow([self.final_string, answer])


# Do you like to....(verb)...?
class DoQuestion1(AIQuestions):
    def __init__(self, s):
        super(DoQuestion1, self).__init__(s)

    def create_random_question(self):
        super().create_random_question()
        self.final_string = ("Do you like to", str(self.verb_list[self.random_verb]), "?")

    def create_topic_question(self):
        super().create_topic_question()
        self.final_string = ("Do you like to", str(self.verb_list[0]), "?")

    def update(self):
        super().update()


# Do you like (noun) ?
class DoQuestion2(AIQuestions):
    def __init__(self, s):
        super(DoQuestion2, self).__init__(s)

    def create_random_question(self):
        super().create_random_question()
        self.final_string = ("Do you like", str(self.noun_list[self.random_noun]), "?")

    def create_topic_question(self):
        super().create_topic_question()
        self.final_string = ("Do you like", str(self.noun_list[0]), "?")

    def update(self):
        super().update()


# Do you (verb) (noun)?
class DoQuestion3(AIQuestions):
    def __init__(self, s):
        super(DoQuestion3, self).__init__(s)

    def create_random_question(self):
        super().create_random_question()
        self.final_string = (
            "Do you", str(self.verb_list[self.random_verb]), str(self.noun_list[self.random_noun]), "?")

    def create_topic_question(self):
        super().create_topic_question()
        self.final_string = ("Do you", str(self.verb_list[0]), str(self.noun_list[0]), "?")

    def update(self):
        super().update()


# What are you (verb-ing)?
class WhatQuestion(AIQuestions):
    def __init__(self, s):
        super(WhatQuestion, self).__init__(s)

    def create_random_question(self):
        super().create_random_question()
        # Make it in -ing form (create another function outside)
        self.final_string = ("What are you", verb_in_gerund(str(self.verb_list[self.random_verb])), "?")

    def create_topic_question(self):
        super().create_topic_question()
        self.final_string = ("What are you", verb_in_gerund(str(self.verb_list[0])), "?")

    def update(self):
        super().update()


# How does it feel to (verb) [as a human]?
class HowQuestion(AIQuestions):
    def __init__(self, s):
        super(HowQuestion, self).__init__(s)

    def create_random_question(self):
        super().create_random_question()
        self.final_string = ("How does it feel to", str(self.verb_list[self.random_verb]), "as a human?")

    def create_topic_question(self):
        super().create_topic_question()
        self.final_string = ("How does it feel to", str(self.verb_list[0]), "as a human?")

    def update(self):
        super().update()


# Why do humans like to (verb)?
class WhyQuestion(AIQuestions):
    def __init__(self, s):
        super(WhyQuestion, self).__init__(s)

    def create_random_question(self):
        super().create_random_question()
        self.final_string = ("Why do humans like to", str(self.verb_list[self.random_verb]), "?")

    def create_topic_question(self):
        super().create_topic_question()
        self.final_string = ("Why do humans like to", str(self.verb_list[0]), "?")

    def update(self):
        super().update()


# Why do humans like to (verb) (noun)?
class WhyQuestion2(AIQuestions):
    def __init__(self, s):
        super(WhyQuestion2, self).__init__(s)

    def create_random_question(self):
        super().create_random_question()
        self.final_string = (
            "Why do humans like to", str(self.verb_list[self.random_verb]), str(self.noun_list[self.random_noun]), "?")

    def create_topic_question(self):
        super().create_topic_question()
        self.final_string = ("Why do humans like to", str(self.verb_list[0]), str(self.noun_list[0]), "?")

    def update(self):
        super().update()


# (verb-ing) a (noun). Have you ever done that?
class HaveYouEverQuestion(AIQuestions):
    def __init__(self, s):
        super(HaveYouEverQuestion, self).__init__(s)

    def create_random_question(self):
        super().create_random_question()
        # Make it in -ing form (create another function outside)
        self.final_string = (verb_in_gerund(str(self.verb_list[self.random_verb])), "a",
                             str(self.noun_list[self.random_noun]), ". Have you ever done that?")

    def create_topic_question(self):
        super().create_topic_question()
        self.final_string = (verb_in_gerund(str(self.verb_list[0])), "a", str(self.noun_list[0]),
                             ". Have you ever done that?")

    def update(self):
        super().update()


# This question is asked after the AI answered the question and wants to redirect the question
class ReboundQuestion(AIQuestions):
    def __init__(self, s):
        super(ReboundQuestion, self).__init__(s)
        self.rebound_string = ""

    def rebound_question(self):
        with open('Questions.csv', mode='r') as csv_file:
            csv_reader = csv.DictReader(csv_file)
            for row in csv_reader:
                if self.user_input.user_question.answer in list(row.values()) and row["Rebound Q"] != "0":
                    return str(row["Rebound Q"])
            return False

    def create_question(self):
        self.rebound_string = self.rebound_question()

        if type(self.rebound_string) != bool:
            self.final_string = (self.rebound_string, "?")

    def create_random_question(self):
        pass

    def create_topic_question(self):
        pass

    def update(self):
        super().update()


# This question is a question inside the "Questions" file, which will be asked to the user
class SavedQuestion(AIQuestions):
    def __init__(self, s):
        super(SavedQuestion, self).__init__(s)
        self.rebound_string = ""

    def create_random_question(self):
        with open('Questions.csv', mode='r') as csv_file:
            csv_reader = csv.DictReader(csv_file)
            for row in csv_reader:
                if str(row["Questions"]) not in short_term_memory_list:
                    self.final_string = str(row["Questions"])
                    break
    

    # This function will find the topic question
    def find_topic_question(self, value):
        with open('Questions.csv', mode='r') as csv_file:
            csv_reader = csv.DictReader(csv_file)
            
            # This will count how many rows have been read, so that if the program doesn't find any mathcing questions, it will re-ask another question
            for row in csv_reader:

                temp = row["Questions"].split()
                temp.append("?")
                
                if value in row["Questions"].split() and join_string(temp) not in self.already_asked_questions:
                    self.final_string = temp
                    break
            
            if str(self.final_string) == "":
                recursion_fix[0] += 1
                #print("pusssyooo")
                #new = choose_question(self.user_input)
                #new.update()


    def create_topic_question(self):
        super().create_topic_question()
        
        if len(object_noun) != 0:
            self.find_topic_question(self.noun_list[0])

        elif len(object_verb) != 0:
            self.find_topic_question(self.verb_list[0])

    def update(self):
        super().update()


# Feeling questions (How are you feeling today?) {This will depend on the emotion of the person}
# - You seem sad. Everything ok? You can talk to me about it if you want!
# - You seem very happy today. Am I right?

# Short questions [This will be "HOW?", "Why?", "HOW?", "REALLY?", "DO YOU?"] {They will depend on the person's sentence}


# Make sure that the sentences that don't make sense but have a meaning, they are corrected
# and associated with the right way of saying it in another csv file

# ======================================================================================