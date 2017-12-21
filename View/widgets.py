from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *


class IntroWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.initStartUI()

    def initStartUI(self):
        train_btn = QPushButton("Train words")
        train_btn.clicked.connect(self.changeToTrainUI)
        train_btn.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        train_btn.setFont(QFont("SansSerif", 20))

        dict_btn = QPushButton("Dictionary")
        dict_btn.clicked.connect(self.changeToDictUI)
        dict_btn.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        dict_btn.setFont(QFont("SansSerif", 20))

        grid = QGridLayout()
        grid.setColumnStretch(0, 1)
        grid.setColumnStretch(1, 3)
        grid.setColumnStretch(2, 1)
        grid.setRowStretch(0, 1)
        grid.setRowStretch(1, 3)
        grid.setRowStretch(2, 1)
        grid.setRowStretch(3, 3)
        grid.setRowStretch(4, 1)
        grid.setSpacing(100)
        grid.addWidget(train_btn, 1, 1)
        grid.addWidget(dict_btn, 3, 1)
        grid.setSpacing(10)

        self.setLayout(grid)
        self.setWindowTitle('DictTrainer')

    def changeToTrainUI(self):
        self.parent().initTrainUI()

    def changeToDictUI(self):
        self.parent().initDictUI()


class TrainWidget(QWidget):
    def __init__(self, word):
        super().__init__()
        self.initStartUI(word)

    def initStartUI(self, word):
        check_btn = QPushButton("CHECK")
        check_btn.clicked.connect(self.checkWord)
        check_btn.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        check_btn.setFont(QFont("SansSerif", 20))

        self.answer_line = QLineEdit()
        self.answer_line.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.answer_line.setFont(QFont("SansSerif", 20))
        self.word_lbl = QLabel(word)
        self.word_lbl.setAlignment(Qt.AlignCenter)
        self.word_lbl.setFont(QFont("SansSerif", 30))

        grid = QGridLayout()
        grid.setColumnStretch(0, 1)
        grid.setColumnStretch(1, 3)
        grid.setColumnStretch(2, 1)
        grid.setRowStretch(0, 2)
        grid.setRowStretch(1, 2)
        grid.setRowStretch(2, 1)
        grid.setRowStretch(3, 1)
        grid.setRowStretch(4, 1)
        grid.setSpacing(100)
        grid.addWidget(self.word_lbl, 0, 1)
        grid.addWidget(check_btn, 1, 1)
        grid.addWidget(self.answer_line, 3, 1)
        grid.setSpacing(10)

        self.setLayout(grid)
        self.setWindowTitle('DictTrainer')

    def checkWord(self):

        if self.parent().model.check_word_translation(self.word_lbl.text(),
                                                      self.answer_line.text()):
            callMsgBox("Correct")
        else:
            callMsgBox("Incorrect")
        self.parent().initTrainUI()


class DictWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.initStartUI()

    def initStartUI(self):
        search_btn = QPushButton("Search")
        search_btn.clicked.connect(self.searchWord)
        search_btn.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        search_btn.setFont(QFont("SansSerif", 20))

        add_btn = QPushButton("Add")
        add_btn.clicked.connect(self.addWord)
        add_btn.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        add_btn.setFont(QFont("SansSerif", 20))

        del_btn = QPushButton("Delete")
        del_btn.clicked.connect(self.deleteWord)
        del_btn.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        del_btn.setFont(QFont("SansSerif", 20))

        mod_btn = QPushButton("Modify")
        mod_btn.clicked.connect(self.modifyWord)
        mod_btn.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        mod_btn.setFont(QFont("SansSerif", 20))

        self.search_line = QLineEdit()
        self.search_line.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.search_line.setFont(QFont("SansSerif", 30))

        self.description_txt = QTextEdit()

        grid = QGridLayout()
        grid.setColumnStretch(0, 1)
        grid.setColumnStretch(1, 1)
        grid.setColumnStretch(2, 1)
        grid.setColumnStretch(3, 1)

        grid.setRowStretch(0, 1)
        grid.setRowStretch(1, 3)
        grid.setRowStretch(2, 1)
        grid.setRowStretch(3, 1)
        grid.addWidget(self.search_line, 0, 0, 1, 3)
        grid.addWidget(search_btn, 0, 3, 1, 1)
        grid.addWidget(self.description_txt, 1, 0, 1, 4)
        grid.addWidget(add_btn, 2, 0, 1, 2)
        grid.addWidget(del_btn, 2, 2, 1, 2)
        grid.addWidget(mod_btn, 3, 0, 2, 2)

        self.setLayout(grid)
        self.setWindowTitle('DictTrainer')

    def searchWord(self):
        accepted_word = self.search_line.text()
        word = self.parent().model.get_word(accepted_word)
        if word:
            self.description_txt.setText("Word : " + word.name + "\nNotes : " + str(word.notes))
        else:
            self.description_txt.setText(
                "There is no such word in " + self.parent().model.dict_from.name + " dictionary")

    def addWord(self):
        pass

    def deleteWord(self):
        pass

    def modifyWord(self):
        pass


def callMsgBox(s):
    msgBox = QMessageBox()
    if s == "Correct":
        msgBox.setIcon(QMessageBox.Question)
    if s == "Incorrect":
        msgBox.setIcon(QMessageBox.Critical)
    msgBox.setText(s)
    msgBox.exec()
