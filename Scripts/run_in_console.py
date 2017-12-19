from Model.dict_objs import Word
from Model.model import Model

bye_message = "Thank you. Bye."


def main():
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
            stop(model)
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
            10: unmark_word,
            0: stop
        }
        switcher[choice](model)


# Next part of code doesn't work
def get_words_list(model):
    print("Words list")
    result = model.get_word()
    for elem in result:
        print(elem)


def get_dicts_list(model):
    print("Dictionaries list")
    result = model.get_dict()
    for elem in result:
        print(elem)


def get_dicts_in_use(model):
    dict1 = model.dict_in
    dict2 = model.dict_out
    print("Translated language is " + dict1.name + \
          ", language to translate in is " + dict2.name)


def get_word_data(model):
    name = input("Word :")
    dict_id = input("Dictionary id :")
    result = model.get_word(word=(name, dict_id))
    if result is not None:
        print(result[0])
    else:
        print("There are no words like this")


def get_dict_data(model):
    name = input("Dictionary name :")
    result = model.get_dict(dictionary=name)
    if result is not None:
        print(result[0])
    else:
        print("There are no dictionaries like this")


def add_word(model):
    name = input("Word :")
    notes = input("Notes(Don't want any, press enter) :")
    dict_id = input("Dictionary ID :")
    mark = input("Mark ( 1 - yes / 0 - no ) :")
    if model.add_word(
            Word(name=name, notes=notes, dict_id=dict_id, mark=mark)) is None:
        print("The word hasn't been added to the dictionary in this iteration")
    else:
        print("The word has been added to the dictionary in this iteration")


def modify_word(model):
    name = input("Word :")
    dict_id = input("Dictionary ID :")
    new_notes = input("New notes :")
    new_dict_id = input("New dict :")
    new_mark = input("New mark :")

    if model.modify_word(Word(name=name, dict_id=dict_id),
                         Word(
                             name=name,
                             notes=new_notes,
                             dict_id=new_dict_id,
                             mark=new_mark)
                         ) is None:
        print("The word hasn't been modified to the dictionary in this iteration")
    else:
        print("The word has been modified to the dictionary in this iteration")


def delete_word(model):
    name = input("Word :")
    dict_id = input("Dictionary ID :")
    if model.del_word(Word(name=name, dict_id=dict_id)) is None:
        print("The word hasn't been deleted from the dictionary in this iteration")
    else:
        print("The word has been deleted from the dictionary in this iteration")


def mark_word(model):
    name = input("Word :")
    dict_id = input("Dictionary ID :")
    if model.mark_word(Word(name=name, dict_id=dict_id)) is None:
        print("The word hasn't been marked from the dictionary in this iteration")
    else:
        print("The word has been marked from the dictionary in this iteration")


def unmark_word(model):
    name = input("Word :")
    dict_id = input("Dictionary ID :")
    if model.unmark_word(Word(name=name, dict_id=dict_id)) is None:
        print("The word hasn't been unmarked from the dictionary in this iteration")
    else:
        print("The word has been unmarked from the dictionary in this iteration")


def stop(model):
    print("Ty for using this dict")
    model.close()

if __name__ == "__main__":
    main()
