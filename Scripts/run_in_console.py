from Model.model import Model

bye_message = "Thank you. Bye."


def main():
    # answer = input("If you want to try console version of this application, write yes : ")
    # answer = answer.lower().strip()
    # if answer != "yes":
    #     print(bye_message)
    #     return

    model = Model("/home/koshachok/src/Dict-translater/Resources/dict_db")

    while True:
        try:
            choise = int(input(
"""
Choose one of the options below
1. Get words list
2. Get dicts list
3. Get dicts in use
4. Get data about the word 
5. Get data about the dict
6. Add word 
7. Modify word
8. Delete word
9. Mark word
10. Unmark word
0. Exit
"""
            ))
            if choise > 10 or choise < 0:
                raise TypeError()
        except TypeError:
            print("You have written wrong data. Try once again.")
            continue
        if choise is 0:
            print(bye_message)
            break

        switcher = {
            1: get_words_list(model),
            2: get_dict_data(model),
            3: get_dicts_in_use(model),
            4: get_word_data(model),
            5: get_dict_data(model),
            6: add_word(model),
            7: modify_word(model),
            8: delete_word(model),
            9: mark_word(model),
            10: unmark_word(model),
        }
        switcher[choise]()

# Next part of code doesn't work
def get_words_list(model):
    print("You've chosen to show the whole words list")
    result = model.get_word()
    for elem in result:
        print(elem)


def get_dicts_list(model):
    print("You've chosen to show the whole words list")
    result = model.get_dict()
    for elem in result:
        print(elem)


def get_dicts_in_use(model):
    dict1 = model.dict_in
    dict2 = model.dict_out
    print("Translated language is " + dict1 +\
          ", language to translate in is " + dict2)


def get_word_data(model):
    pass


def get_dict_data(model):
    pass


def add_word(model):
    pass


def modify_word(model):
    pass


def delete_word(model):
    pass


def mark_word(model):
    pass


def unmark_word(model):
    pass


if __name__ == "__main__":
    main()
