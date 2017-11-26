import sqlite3

from Model.dict_objs import Word


def singleton(cls):
    instances = {}

    def getinstance():
        if cls not in instances:
            instances[cls] = cls()
        return instances[cls]

    return getinstance


@singleton
class Model:
    sql_switcher = {"Add word": "",
                    "Get word": "",
                    "Del word": "",
                    "Modify word": "",
                    "Mark word": "",
                    "Unmark word": "",
                    "Get marked words": ""
                    }

    def __init__(self, db_name):
        self.db_name = db_name

    def __str__(self):
        return "You are working with Data Base : " + self.db_name

    def get_word(self, words, cursor):
        result = list()
        try:
            for word in words:
                cursor.execute(Model.sql_switcher["Get word"],
                               (word.id, word.dict_id))
                line = cursor.fetchone()[0]
                result.append(Word(line[0], line[1], line[2], line[3], line[4]))
        except sqlite3.DatabaseError as err:
            print("Eroor: ", err)
        else:
            return result

    def word_fn(self, word, query):
        try:
            conn = sqlite3.connect(self.db_name)
            cursor = conn.cursor()

            if len(self.get_word(word, cursor)) is 0:
                return False

            cursor.execute(query,
                           (word.name, word.notes, word.dict_id, word.mark))
        except sqlite3.DatabaseError as err:
            print("Error: ", err)
        else:
            conn.commit()
            return True

    def add_word(self, word):
        return self.word_fn(word, Model.sql_switcher["Add word"])

    def del_word(self, word):
        return self.word_fn(word, Model.sql_switcher["Del word"])

    def modify_word(self, word):
        return self.word_fn(word, Model.sql_switcher["Modify word"])

    def mark_word(self, word):
        return self.word_fn(word, Model.sql_switcher["Mark word"])

    def unmark_word(self, word):
        return self.word_fn(word, Model.sql_switcher["Unmark word"])

# "Get marked words" method requiered