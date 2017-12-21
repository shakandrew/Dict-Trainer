import random

from PyQt5.QtCore import QAbstractItemModel

from DBAPI.db_api import DBApi
from DBAPI.db_api_obejcts import *


# from DBAPI.db_api_obejcts import *


class Model(QAbstractItemModel):
    def __init__(self):
        super().__init__()
        self.api = DBApi("../Resources/dict_db")
        self.dict_from = self.get_dict("English")
        self.dict_to = self.get_dict("Polish")

    def data(self, index, role=None):
        pass

    def get_dict(self, dict_name):
        return self.api.get_dict([], dict_name)[0]

    def get_dict_all(self):
        return self.api.get_dict([])

    def get_word(self, word_name):
        word = self.api.get_word([], (word_name, self.dict_from.id))
        if word:
            return word[0]
        else:
            return None

    def get_word_all(self):
        return self.api.get_word([])

    def get_translation(self, word_name):
        words = self.get_translation_pairs()
        if word_name in words:
            return words[word_name]

    def add_word(self, word):
        self.api.add_word(Word(word, self.dict_from.id))

    def delete_word(self, word):
        self.api.del_word(Word(word, self.dict_from.id))

    def modify_word(self, word, new_notes, new_mark):
        self.api.modify_word(Word(word, self.dict_from.id),
                             new_notes=new_notes, new_mark=new_mark)

    # Returns str or None
    def get_random_word(self):
        words = self.get_translation_pairs(marked=True)
        if words:
            return random.choice(list(words))
        else:
            return None

    def check_word_translation(self, word_from, word_to):
        words = self.get_translation_pairs(marked=True)
        if (word_from in words and words[word_from] == word_to) or \
                (word_to in words and words[word_to] == word_from):
            return True
        else:
            return False

    def get_translation_pairs(self, marked=False):
        all_words = self.api.get_word({}, marked=marked)
        all_translations = self.api.get_translation()
        words = {}
        if all_words and all_translations:
            for translation in all_translations:
                word_1 = all_words[translation.word_1]
                word_2 = all_words[translation.word_2]
                if word_1.dict_id == self.dict_from.id and \
                        word_2.dict_id == self.dict_to.id:
                    words[word_1.name] = word_2.name
        return words
