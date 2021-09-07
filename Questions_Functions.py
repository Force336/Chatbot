
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

# This function will create a random question
def choose_random_question():
    number = random.randint(1, 8)
    if number == 1:
        x = DoQuestion1()
    elif number == 2:
        x = DoQuestion2()
    elif number == 3:
        x = DoQuestion3()
    elif number == 4:
        x = WhatQuestion()
    elif number == 5:
        x = HowQuestion()
    elif number == 6:
        x = WhyQuestion()
    elif number == 7:
        x = WhyQuestion2()
    else:
        x = HaveYouEverQuestion()
    return x

# This function will determine which question the AI will use next
def choose_question(user_input_par):

    x = 0
    # Choosing topic questions
    verb_and_noun_object_determinate()
    if (len(object_verb) != 0 or len(object_noun) != 0) and recursion_fix[0] < recursion_fix[1]:
        if len(object_verb) != 0 and len(object_noun) != 0:
            x = choose_random_question()
        elif len(object_verb) != 0 and len(object_noun) == 0:
            number = random.randint(1, 3)
            if number == 1:
                x = DoQuestion1()
            elif number == 2:
                x = WhatQuestion()
            elif number == 3:
                x = WhyQuestion()

        # elif object_verb is None and object_noun is not None:
        else:
            x = DoQuestion2()

    # Choosing random questions
    else:
        if recursion_fix[0] == recursion_fix[1]:
            object_noun.clear(), object_verb.clear()
        x = choose_random_question()

    # Creates a Rebound question and it checks if it's there or not
    if type(user_input_par.user_question) is UserQuestions:
        y = ReboundQuestion(user_input_par)
        y.create_question()

        if type(y.rebound_string) != bool:
            x = y

    return x
# -----------------------------------------