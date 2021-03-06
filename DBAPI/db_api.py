import sqlite3

from DBAPI.db_api_obejcts import Word, Dictionary, Translation


def singleton(cls):
    instances = {}

    def getinstance():
        if cls not in instances:
            instances[cls] = cls()
        return instances[cls]

    return getinstance


# @singleton
class DBApi:
    def __init__(self, db_name):
        self.db_name = db_name

        self.conn = None
        self.cursor = None
        self.update_connection()

    def __str__(self):
        return "You are working with Data Base : " + self.db_name

    def exec_fn(self, query, args=None):
        try:
            if args is None:
                self.cursor.execute(query)
            else:
                self.cursor.execute(query, args)
        except sqlite3.DatabaseError as err:
            print("Error: " + str(err) + "\nWhile trying to execute:\n" + \
                  query + "\nDataBase connection has been reloaded")
            self.update_connection()
        else:
            self.conn.commit()

    # Add word into the DB
    # IN : object of Word() / str query
    # OUT : None/True
    def add_word(self, word, query=None):
        if query is None:
            query = self.sql_switcher["Add word"]
        if self.get_word([], word=(word.name, word.dict_id)):
            self.exec_fn(query, args=(word.name, word.notes, word.dict_id, word.mark))

    # Deletes word from the DB
    # IN : object of Word() / str query
    # OUT : None/True
    def del_word(self, word, query=None):
        if query is None:
            query = self.sql_switcher["Del word"]
        if self.get_word([], word=(word.name, word.dict_id)):
            self.exec_fn(query, args=(word.name, word.dict_id))

    # Modify word in the DB
    # IN : object of Word() / str new_notes / 1\0 new_mark / str query
    # OUT : None/True
    def modify_word(self, word, new_notes=None, new_mark=None, query=None):
        if query is None:
            query = self.sql_switcher["Modify word"]
        temp = self.get_word([], word=(word.name, word.dict_id))
        if temp:
            if new_notes is None:
                new_notes = temp[0].notes
            if new_mark is None:
                new_mark = temp[0].mark
            self.exec_fn(query, args=(new_notes, new_mark, word.name, word.dict_id))

    # Mark word in the DB
    # IN : object of Word()
    # OUT : None/True
    def mark_word(self, word):
        self.modify_word(word, new_mark=1, query=self.sql_switcher["Mark word"])

    # Modify word in the DB
    # IN : object of Word()
    # OUT : None/True
    def unmark_word(self, word):
        self.modify_word(word, new_mark=0, query=self.sql_switcher["Unmark word"])

    def add_translation(self, word1, word2):
        if word1 and word2:
            # pair word_1 - word_2
            transl = self.get_translation((word1, word2))
            if not transl:
                self.exec_fn(self.sql_switcher["Add translation"], args=(word1, word2))
            # pair word_2 - word_1
            transl = self.get_translation((word2, word1))
            if not transl:
                self.exec_fn(self.sql_switcher["Add translation"], args=(word2, word1))

        return None

    def del_translation(self, word1, word2):
        if word1 and word2:
            # pair word_1 - word_2
            transl = self.get_translation((word1, word2))
            if transl:
                self.exec_fn(self.sql_switcher["Del translation"], args=(word1, word2))
            # pair word_2 - word_1
            transl = self.get_translation((word2, word1))
            if transl:
                self.exec_fn(self.sql_switcher["Del translation"], args=(word2, word1))

        return None

    def close(self):
        self.conn.commit()
        self.cursor.close()
        self.conn.close()

    def update_connection(self):
        if self.cursor is not None:
            self.cursor.close()
        if self.conn is not None:
            self.conn.close()
        self.conn = sqlite3.connect(self.db_name)
        self.cursor = self.conn.cursor()

    # Expects None or (word.name, word.dict_id)
    # Returns list of word(s) | None if no data
    # If words = None, it will return all words ( words = list() )
    # If marked = True, it will return only marked words ( marked = Bool )
    def get_word(self, collection, word=None, marked=False):
        query = ""
        if marked is True:
            query = DBApi.sql_switcher["Marked suffix"].format(1)
        try:
            if word is None:
                query = DBApi.sql_switcher["Get all words"] + query
            else:
                query = (DBApi.sql_switcher["Get word"] + query).format(word)

            self.cursor.execute(query)
            lines = self.cursor.fetchall()
            for line in lines:
                collection = self.to_collection(
                    collection,
                    Word(id=line[0], name=line[1], notes=line[2], dict_id=line[3], mark=line[4])
                )
        except sqlite3.DatabaseError as err:
            print("Error: " + str(err) + "\nDataBase connection has been reloaded")
            self.update_connection()
        else:
            return collection

    # Returns list of dictionary(-ies) | None if no data
    # If dictionaries = None, it will return all dictionaries ( dictionaries = str() )
    def get_dict(self, collection, dictionary=None):
        query = ""
        try:
            if dictionary is None:
                query = DBApi.sql_switcher["Get all dicts"]
            else:
                query = DBApi.sql_switcher["Get dict"].format(dictionary)
            self.cursor.execute(query)
            lines = self.cursor.fetchall()
            for line in lines:
                collection = self.to_collection(
                    collection,
                    Dictionary(id=line[0], name=line[1])
                )
        except sqlite3.DatabaseError as err:
            print("Error: " + str(err) + "\nDataBase connection has been reloaded")
            self.update_connection()
        else:
            return collection

    def get_translation(self, translation=None):
        result = []
        query = ""
        try:
            if translation is None:
                query = DBApi.sql_switcher["Get all translations"]
            else:
                query = DBApi.sql_switcher["Get translation"].format(translation)
            self.cursor.execute(query)
            lines = self.cursor.fetchall()
            for line in lines:
                result.append(Translation(line[0], line[1]))
        except sqlite3.DatabaseError as err:
            print("Error: " + str(err) + "\nDataBase connection has been reloaded")
            self.update_connection()
        else:
            return result

    def to_collection(self, collection, obj):
        if type(collection) == type([]):
            collection.append(obj)
        if type(collection) == type({}):
            collection[obj.id] = obj
        return collection

    sql_switcher = {
        "Add word": "INSERT INTO Word (name, notes, dict_id, mark) "
                    "VALUES (?, ?, ?, ?);",
        "Del word": "DELETE FROM Word WHERE name=? AND dict_id=? ",
        "Modify word": "UPDATE Word SET notes=?, mark=? "
                       "WHERE name=? AND dict_id=? ",
        "Mark word": "UPDATE Word SET mark = 1 WHERE name=? AND dict_id=? ",
        "Unmark word": "UPDATE Word SET mark = 0 WHERE name=? AND dict_id=? ",
        "Marked suffix": "WHERE mark={} ",
        "Add translation": "INSERT INTO Translation VALUES (?,?)",
        "Del translation": "DELETE FROM Translation WHERE id_1=? and id_2=?",
        # <GETBLOCK>
        # Note: suffix will be added, that why there is no ';'
        "Get word": "SELECT * FROM Word WHERE name='{0[0]}' AND dict_id={0[1]} ",
        # Note: suffix will be added, that why there is no ';'
        "Get all words": "SELECT * FROM Word ",
        "Get dict": "SELECT * FROM Dictionary WHERE name='{0}' ",
        "Get all dicts": "SELECT * FROM Dictionary ",
        "Get translation": "SELECT * FROM Translation WHERE id_1={0[0]} and id_2={0[1]}",
        "Get all translations": "SELECT * FROM Translation"
        # </GETBLOCK>
    }
