class Dictionary:
    def __init__(self, name, id=0):
        self.id = id
        self.name = name

    def __str__(self):
        id = "ID = {}; ".format(self.id)
        name = "Name = {} ".format(self.name)
        return id + name

    def __eq__(self, other):
        if other.name == self.name:
            return True
        else:
            return False

    def __name__(self):
        return "Dictionary"


class Word:
    def __init__(self, name, dict_id, mark=0, notes=None, id=None):
        self.id = id
        self.name = name
        self.notes = notes
        self.dict_id = dict_id
        self.mark = mark

    def __str__(self):
        id = "ID = {}; ".format(self.id)
        name = "Name = {}; ".format(self.name)
        notes = ("Notes = {}; ".format(self.notes)) if self.notes is not None else ""
        dict_id = "Dictionary ID = {}; ".format(self.dict_id)
        mark = "Mark = {};".format(self.mark)
        return id + name + notes + dict_id + mark

    def __eq__(self, other):
        if other.name == self.name and other.dict_id == self.dict_id:
            return True
        else:
            return False

    def __name__(self):
        return "Word"


class Translation:
    def __init__(self, word_1, word_2):
        self.word_1 = word_1
        self.word_2 = word_2

    def __str__(self):
        return "First word ID = " + str(self.word_1) + \
               "; Second word ID = " + str(self.word_2)

    def __eq__(self, other):
        if other.word_1 == self.word_1 and other.word_2 == self.word_2:
            return True
        else:
            return False

    def __name__(self):
        return "Translation"
