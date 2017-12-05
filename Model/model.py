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

        self.dict_out = self.get_dict("English")[0]
        self.dict_in = self.get_dict("Polish")[0]

    def __str__(self):
        return "You are working with Data Base : " + self.db_name

    def word_fn(self, word, query, args):
        try:
            self.cursor.execute(query, args)
        except sqlite3.DatabaseError as err:
            print("Error: " + str(err) + "\nWhile trying to execute:\n" + \
                  query + "\nDataBase connection has been reloaded")
            self.update_connection()
            return None
        else:
            self.conn.commit()
            return True

    def add_word(self, word):
        if self.get_word(word=(word.name, word.dict_id)) is not None:
            return None
        return self.word_fn(word,
                            self.sql_switcher["Add word"],
                            (word.name, word.notes, word.dict_id, word.mark))

    def del_word(self, word):
        if self.get_word(word=(word.name, word.dict_id)) is None:
            return None
        return self.word_fn(word,
                            self.sql_switcher["Del word"],
                            (word.name, word.dict_id))

    def modify_word(self, word_old, word_new):
        if (word_old.dict_id != word_new.dict_id and self.get_word(
                word=(word_new.name, word_new.dict_id)) is not None) or \
                        self.get_word(word=(word_old.name, word_old.dict_id)) is None:
            return None
        return self.word_fn(word_new,
                            self.sql_switcher["Modify word"],
                            (word_new.name, word_new.notes,
                             word_new.dict_id, word_new.mark,
                             word_old.name, word_old.dict_id))

    def mark_word(self, word):
        if self.get_word((word.name, word.dict_id)) is None:
            return None
        return self.word_fn(word,
                            self.sql_switcher["Mark word"],
                            (word.name, word.dict_id))

    def unmark_word(self, word):
        if self.get_word((word.name, word.dict_id)) is None:
            return None
        return self.word_fn(word,
                            self.sql_switcher["Unmark word"],
                            (word.name, word.dict_id))

    def update_connection(self):
        if self.cursor is not None:
            self.cursor.close()
        if self.conn is not None:
            self.conn.close()
        self.conn = sqlite3.connect(self.db_name)
        self.cursor = self.conn.cursor()

    # TODO fix errors
    # Returns list of word(s) | None if no data
    # If words = None, it will return all words ( words = list() )
    # If marked = True, it will return only marked words ( marked = Bool )
    def get_word(self, word=None, marked=False):
        result = None
        query = ""
        if marked is True:
            query = Model.sql_switcher["Marked suffix"].format(1)
        try:
            if word is None:
                query = Model.sql_switcher["Get all words"] + query
            else:
                query = (Model.sql_switcher["Get word"] + query).format(word)

            self.cursor.execute(query)
            lines = self.cursor.fetchall()
            if len(lines) != 0:
                result = []
                for line in lines:
                    result.append(Word(
                        id=line[0],
                        name=line[1],
                        notes=line[2],
                        dict_id=line[3],
                        mark=line[4]
                    ))
        except sqlite3.DatabaseError as err:
            print("Error: " + str(err) + "\nDataBase connection has been reloaded")
            self.update_connection()
        else:
            return result

    # Returns list of dictionary(-ies) | None if no data
    # If dictionaries = None, it will return all dictionaries ( dictionaries = str() )
    def get_dict(self, dictionary=None):
        result = None
        query = ""
        try:
            if dictionary is None:
                query = Model.sql_switcher["Get all dicts"]
            else:
                query = Model.sql_switcher["Get dict"].format(dictionary)
            self.cursor.execute(query)
            lines = self.cursor.fetchall()
            if len(lines) != 0:
                result = []
                for line in lines:
                    result.append(Dictionary(
                        id=line[0],
                        name=line[1]
                    ))
        except sqlite3.DatabaseError as err:
            print("Error: " + str(err) + "\nDataBase connection has been reloaded")
            self.update_connection()
        else:
            return result

    def translate_word(self, word):
        pass

    def close(self):
        self.conn.commit()
        self.cursor.close()
        self.conn.close()

    sql_switcher = {
        "Add word": "INSERT INTO Word (name, notes, dict_id, mark) "
                    "VALUES (?, ?, ?, ?);",
        "Del word": "DELETE FROM Word WHERE name=? AND dict_id=? ",
        "Modify word": "UPDATE Word SET name=?, notes=?, dict_id=?, mark=? "
                       "WHERE name=? AND dict_id=? ",
        "Mark word": "UPDATE Word SET mark = 1 WHERE name=? AND dict_id=? ",
        "Unmark word": "UPDATE Word SET mark = 0 WHERE name=? AND dict_id=? ",
        "Marked suffix": "WHERE mark={} ",
        # Note: suffix will be added, that why there is no ';'
        "Get word": "SELECT * FROM Word WHERE name='{0[0]}' AND dict_id={0[1]} ",
        # Note: suffix will be added, that why there is no ';'
        "Get all words": "SELECT * FROM Word ",
        "Get dict": "SELECT * FROM Dictionary WHERE name='{0}' ",
        "Get all dicts": "SELECT * FROM Dictionary "
    }
