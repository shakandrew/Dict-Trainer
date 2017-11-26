class Dictionary:
    def __init__(self, id, name):
        self.id = id
        self.name = name

    def __str__(self):
        return "ID = " + str(self.id) + " Name = " + self.name

    def __eq__(self, other):
        if other.id == self.id and other.name == self.name:
            return True
        else:
            return False

    def __name__(self):
        return "Dictionary"


class Word:
    def __init__(self, id, name, notes, dict_id, mark):
        self.id = id
        self.name = name
        self.notes = notes
        self.dict_id = dict_id
        self.mark = mark

    def __str__(self):
        return "ID = " + str(self.id) + " Name = " + self.name + " Notes = " + self.notes + \
               " Dict_ID = " + self.dict_id + " Mark = " + self.mark

    def __eq__(self, other):
        if other.id == self.id and other.name == self.name and other.dict_id == self.dict_id:
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
        return "First word ID = " + str(self.word_1) + "; Second word ID =" + str(self.word_2)

    def __eq__(self, other):
        if other.word_1 == self.word_1 and other.word_2 == self.word_2:
            return True
        else:
            return False

    def __name__(self):
        return "Translation"