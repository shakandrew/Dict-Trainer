import sqlite3

from Model.dict_objs import Word, Dictionary, Translation


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
                    "Get all words": "",
                    "Del word": "",
                    "Modify word": "",
                    "Mark word": "",
                    "Unmark word": "",
                    "Marked suffix": "",
                    "Get dict": "",
                    "Get all dicts": ""
                    }

    def __init__(self, db_name):
        self.db_name = db_name
        self.dict_out = self.get_dict("English")
        self.dict_in = self.get_dict("Polish")

    def __str__(self):
        return "You are working with Data Base : " + self.db_name

    # Returns list of words
    # If words = None, it will return all words ( words = list() )
    # If marked = True, it will return only marked words ( marked = Bool )
    @staticmethod
    def get_word(cursor, words=None, marked=False):
        result = list()
        suffix = None
        if marked is True:
            suffix = Model.sql_switcher["Marked suffix"] % {"Some vars": "will be there"}
        try:
            if words is None:
                cursor.execute(Model.sql_switcher["Get all words"] + suffix)
                for line in cursor.fetchall():
                    result.append(Word(line[0], line[1], line[2], line[3], line[4]))
            else:
                for word in words:
                    cursor.execute(Model.sql_switcher["Get word"] + suffix,
                                   (word[0], word[1]))
                    line = cursor.fetchone()[0]
                    result.append(Word(line[0], line[1], line[2], line[3], line[4]))
        except sqlite3.DatabaseError as err:
            print("Error: ", err)
        else:
            return result

    def word_fn(self, word, query):
        try:
            conn = sqlite3.connect(self.db_name)
            cursor = conn.cursor()

            if len(self.get_word(cursor, words=(word.name, word.dict_id))) is 0:
                return False

            cursor.execute(query,
                           (word.name, word.notes, word.dict_id, word.mark))
        except sqlite3.DatabaseError as err:
            print("Error: ", err)
        else:
            conn.commit()
            return True

    def add_word(self, word):
        return self.word_fn(word, self.sql_switcher["Add word"])

    def del_word(self, word):
        return self.word_fn(word, self.sql_switcher["Del word"])

    def modify_word(self, word):
        return self.word_fn(word, self.sql_switcher["Modify word"])

    def mark_word(self, word):
        return self.word_fn(word, self.sql_switcher["Mark word"])

    def unmark_word(self, word):
        return self.word_fn(word, self.sql_switcher["Unmark word"])

    # Returns list of dictionaries
    # If dictionaries = None, it will return all dictionaries ( dictionaries = str() )
    def get_dict(self, dictionaries=None):
        result = list()
        try:
            cursor = sqlite3.connect(self.db_name).cursor()
            if dictionaries is None:
                cursor.execute(self.sql_switcher["Get all dicts"])
                for line in cursor.fetchall():
                    result.append(Dictionary(line[0], line[1]))
            else:
                for dictionary in dictionaries:
                    cursor.execute(Model.sql_switcher["Get word"],
                                   (dictionary,))
                    line = cursor.fetchone()[0]
                    result.append(Word(line[0], line[1], line[2], line[3], line[4]))
        except sqlite3.DatabaseError as err:
            print("Error: ", err)
        else:
            return result


