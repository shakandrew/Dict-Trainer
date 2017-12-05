import sqlite3

from Model.dict_objs import Word, Dictionary


def singleton(cls):
    instances = {}

    def getinstance():
        if cls not in instances:
            instances[cls] = cls()
        return instances[cls]

    return getinstance


# @singleton
class Model:
    def __init__(self, db_name):
        self.db_name = db_name

        self.conn = None
        self.cursor = None
        self.update_connection()

        self.dict_out = self.get_dict(("English",))
        self.dict_in = self.get_dict(("Polish",))

    def __str__(self):
        return "You are working with Data Base : " + self.db_name

    def word_fn(self, word, query, args):
        try:
            if len(self.get_word(words=(word.name, word.dict_id))) is 0:
                return False
            self.cursor.execute(query, args)
        except sqlite3.DatabaseError as err:
            print("Error: " + str(err) + "\nDataBase connection has been reloaded")
            self.update_connection()
        else:
            self.conn.commit()
            return True

    def add_word(self, word):
        return self.word_fn(word,
                            self.sql_switcher["Add word"],
                            (word.name, word.notes, word.dict_id, word.mark))

    def del_word(self, word):
        return self.word_fn(word,
                            self.sql_switcher["Del word"],
                            (word.name, word.dict_id))

    def modify_word(self, word_old, word_new):
        return self.word_fn(word_new,
                            self.sql_switcher["Modify word"],
                            (word_new.name, word_new.notes,
                             word_new.dict_id, word_new.mark,
                             word_old.name, word_old.dict_id))

    def mark_word(self, word):
        return self.word_fn(word,
                            self.sql_switcher["Mark word"],
                            (word.name, word.dict_id))

    def unmark_word(self, word):
        return self.word_fn(word,
                            self.sql_switcher["Unmark word"],
                            (word.name, word.dict_id))

    def update_connection(self):
        if self.conn is not None:
            self.conn.close()
        if self.cursor is not None:
            self.cursor.close()
        self.conn = sqlite3.connect(self.db_name)
        self.cursor = self.conn.cursor()

    # TODO fix errors
    # Returns list of words
    # If words = None, it will return all words ( words = list() )
    # If marked = True, it will return only marked words ( marked = Bool )
    def get_word(self, words=None, marked=False):
        result = list()
        suffix = ""
        if marked is True:
            suffix = Model.sql_switcher["Marked suffix"] % \
                     {"arg1": 1}
        suffix += ";"
        try:
            if words is None:
                self.cursor.execute(Model.sql_switcher["Get all words"] +\
                                    suffix)
                for line in self.cursor.fetchall():
                    result.append(Word(
                        id=line[0],
                        name=line[1],
                        notes=line[2],
                        dict_id=line[3],
                        mark=line[4])
                    )
            else:
                for word in words:
                    self.cursor.execute(Model.sql_switcher["Get word"] +\
                                        suffix, (word[0], word[1]))
                    line = self.cursor.fetchone()[0]
                    result.append(Word(
                        id=line[0],
                        name=line[1],
                        notes=line[2],
                        dict_id=line[3],
                        mark=line[4])
                    )
        except sqlite3.DatabaseError as err:
            print("Error: " + str(err) + "\nDataBase connection has been reloaded")
            self.update_connection()
        else:
            return result

    # Returns list of dictionaries
    # If dictionaries = None, it will return all dictionaries ( dictionaries = str() )
    def get_dict(self, dictionaries=None):
        result = list()
        try:
            if dictionaries is None:
                self.cursor.execute(Model.sql_switcher["Get all dicts"])
                for line in self.cursor.fetchall():
                    result.append(Dictionary(line[0], line[1]))
            else:
                for dictionary in dictionaries:
                    # o = Model.sql_switcher["Get dict"].format(dictionary)
                    self.cursor.execute(Model.sql_switcher["Get dict"],
                                        (dictionary,))
                    line = self.cursor.fetchone()
                    result.append(Dictionary(line[0], line[1]))
        except sqlite3.DatabaseError as err:
            print("Error: " + str(err) + "\nDataBase connection has been reloaded")
            self.update_connection()
        else:
            return result

    sql_switcher = {
        "Add word": "INSERT INTO Word (name, notes, dict_id, mark) "
                    "VALUES (?, ?, ?, ?);",
        # Note: suffix will be added, that why there is no ';'
        "Get word": "SELECT * FROM Word WHERE name=?, dict_id=? ",
        # Note: suffix will be added, that why there is no ';'
        "Get all words": "SELECT * FROM Word ",
        "Del word": "DELETE FROM Word WHERE name=? AND dict_id=?;",
        "Modify word": "UPDATE Word SET name=?, notes=?, dict_id=?, mark=? "
                       "WHERE name=? AND dict_id=?",
        "Mark word": "UPDATE Word SET mark = 1 WHERE name=? AND dict_id=?;",
        "Unmark word": "UPDATE Word SET mark = 0 WHERE name=? AND dict_id=?;",
        "Marked suffix": "WHERE mark=arg1",
        "Get dict": "SELECT * FROM Dictionary WHERE name=?;",
        "Get all dicts": "SELECT * FROM Dictionary;"
    }
