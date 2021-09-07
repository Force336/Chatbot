# importing modules
import numpy as np
import csv
import pandas as pd

# ================================================================================== Functions ================================================================================================================


# This function checks if a certain question has already been asked before
def stop_repeated_q(my_list):
    """""
    This function reads and checks if there are any repeated random combinations
    in the Already asked Questions Combinations file
    """""

    with open('Already Asked Question Combinations.csv', mode='r') as csv_file:
        csv_reader = csv.DictReader(csv_file)
        for row in csv_reader:
            my_list.append(row["Combinations"])


# This function checks if a certain combination for an AI question is allowed or not
def stop_future_unwanted_q(my_list):
    """""
    This function reads and checks if there are any unwanted combinations
    in the Wrong Questions Combinations file
    """""

    with open('Wrong Questions Combinations.csv', mode='r') as csv_file:
        csv_reader = csv.DictReader(csv_file)
        for row in csv_reader:
            my_list.append(row["Combinations"])


# This function checks if a certain combination can be written in a better way
def better_combination_q(my_list):
    """""
    This function reads and checks if there are any better combinations
    in the Better Questions Combinations file
    """""

    with open('Better Question Combinations.csv', mode='r') as csv_file:
        csv_reader = csv.DictReader(csv_file)
        for row in csv_reader:
            my_list.append((row["old"], row["new"]))


# This function joins a string
def join_string(string):
    return " ".join(string)


# This function turns any value into a value between 0 and 1
def sigmoid(x):
    """
    Takes in weighted sum of the inputs and normalizes
    them through between 0 and 1 through a sigmoid function
    """
    return 1 / (1 + np.exp(-x))


# This returns a percentage of one value over the other
def percentage(x, y):
    value = 0
    try:
        value = x / y * 100
    except ZeroDivisionError:
        value = 0

    return value


# This procedure makes the user input their own answer for the question they asked and the computer failed to answer correctly
def better_questions_answers(question):
    answer = input()

    # Whether or not the question already has a better answer
    local_state = False
    # counts what index the question is found on
    counter = -1

    if answer != "":
        with open('Questions.csv', mode='r') as csv_file:
            csv_reader = csv.DictReader(csv_file)

            for row in csv_reader:
                counter += 1
                if row["Questions"].lower() == question.sentence.lower():

                    my_row = remove_none_list(list(row.values()))
                    my_row = remove_spaces_list(my_row)
                    my_row.append(answer)

                    # Deleting the old row
                    question_file = pd.read_csv("Questions.csv")
                    question_file.drop(question_file.index[[counter]], inplace=True)
                    question_file.to_csv("Questions.csv", index=False)

                    # Adding the new row with the new answer
                    with open('Questions.csv', mode='a', newline='') as csv_write:
                        wtr = csv.writer(csv_write, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
                        wtr.writerow(my_row)

                    local_state = True
                    break

        if not local_state:
            with open('Questions.csv', mode='a', newline='') as csv_file:
                wtr = csv.writer(csv_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
                wtr.writerow([question.sentence, 0, answer])


# This turns a verb into a -ing form verb
def verb_in_gerund(verb):
    length = len(verb)
    if verb[length - 2] == 'i' and verb[length - 1] == 'e':
        verb = verb[:-2]
        verb = ''.join(verb + 'y')

    elif verb[length - 1] == 'e':
        verb = verb[:-1]

    return "".join(verb + "ing")


# This finds how close each user word is to the saved question, and gives a percentage (SHORT SENTENCES)
def question_percentage(my_input, common_question):

    # This will check if the two are exactly the same or not
    if my_input == common_question:
        return percentage(len(my_input), len(common_question))

    else:
        temp1 = set(my_input) & set(common_question)
        temp2 = sorted(temp1, key=lambda k: my_input.index(k))

        return (percentage(len(temp2), len(my_input)) + percentage(len(temp2), len(
            common_question))) / 2


#  This finds if the saved question is in the asked question of the user. (LONG SENTENCES)
def question_match(my_input, common_question):
    if common_question in my_input:
        return True


# Turns a list from ("string 1", "", "", "", "", "string 2") ------> ("string 1", "string 2")
def remove_spaces_list(my_list):
    k = []
    for i in my_list:
        if i.strip():
            k.append(i)
    return k


# Turns a list from ("string 1", None, None, None, None, "string 2") ------> ("string 1", "string 2")
def remove_none_list(my_list):
    k = []
    for i in my_list:
        if i is not None:
            k.append(i)
    return k


# Finds best match from a csv file and user_input
def finding_best_match(row, column_name, my_input, spaces):
    my_tuple = [question_percentage(my_input, row[column_name].split()), str(row[column_name].split())]

    # Checks word for word
    for i in range(len(list(row.values())) - spaces):
        if list(row.values())[i + spaces] != '' and list(row.values())[i + spaces] is not None:
            my_tuple.append(list(row.values())[i + spaces])

    tuple(my_tuple)

    return my_tuple


# =============================================================================================================================================================================================================
# ================================================================================== Variables ================================================================================================================
