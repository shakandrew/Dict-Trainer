from Model.model import Model
from Model.dict_objs import Word, Dictionary

bye_message = "Thank you. Bye."


def main():
    # answer = input("If you want to try console version of this application, write yes : ")
    # answer = answer.lower().strip()
    # if answer != "yes":
    #     print(bye_message)
    #     return

    model = Model("../Resources/dict_db")

    while True:
        try:
            choice = int(input(
                "Choose one of the options below :\n"
                "1. Get words list\n"
                "2. Get dicts list\n"
                "3. Get dicts in use\n"
                "4. Get data about the word\n"
                "5. Get data about the dict\n"
                "6. Add word\n"
                "7. Modify word\n"
                "8. Delete word\n"
                "9. Mark word\n"
                "10. Unmark word\n"
                "0. Exit\n"
            ))
            if choice > 10 or choice < 0:
                raise TypeError()
        except TypeError:
            print("You have written wrong data. Try once again.")
            continue
        if choice is 0:
            print(bye_message)
            break

        switcher = {
            1: get_words_list,
            2: get_dicts_list,
            3: get_dicts_in_use,
            4: get_word_data,
            5: get_dict_data,
            6: add_word,
            7: modify_word,
            8: delete_word,
            9: mark_word,
            10: unmark_word
        }
        switcher[choice](model)


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
    print("Translated language is " + dict1.name + \
          ", language to translate in is " + dict2.name)


def get_word_data(model):
    name = input("Please, write word name :")
    dict_id = input("Please, write dictionary id :")
    result = model.get_word(word=(name, dict_id))
    print(result[0])


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
