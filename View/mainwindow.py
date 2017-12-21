from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import *

from View.widgets import IntroWidget, TrainWidget, DictWidget, callMsgBox


class MainWindow(QMainWindow):
    def __init__(self, model):
        super().__init__()
        self.model = model
        self.initWindowFrame()
        self.initIntroWidget()
        self.setWindowTitle("DictTrainer")
        self.setGeometry(300, 300, 600, 600)
        self.show()

    def initWindowFrame(self):
        exitAction = QAction(QIcon('../Resources/exit.png'), 'StartScreen', self)
        exitAction.triggered.connect(self.initIntroWidget)

        self.toolbar = self.addToolBar('StartScreen')
        self.toolbar.addAction(exitAction)

        # lng_btn_left = QToolButton()
        # for i in self.model.get_dict_all():
        #     act = QAction(QIcon('../Resources/'+i.name+'.png'), i.name, self)
        #     act.triggered.connect(self.changeLanguage)
        #     lng_btn_left.addAction(act)
        #
        # lng_btn_right = QToolButton()
        # for i in self.model.get_dict_all():
        #     act = QAction(QIcon('../Resources/' + i.name + '.png'), i.name, self)
        #     act.triggered.connect(self.changeLanguage)
        #     lng_btn_right.addAction(act)
        #
        # self.toolbar.addAction(lng_btn_left)

    def initIntroWidget(self):
        self.setCentralWidget(IntroWidget())

    def initTrainUI(self):
        word = self.model.get_random_word()
        if word is None:
            callMsgBox("There are no enough data, please fill some in the dictionary")
            return
        else:
            self.setCentralWidget(TrainWidget(word))

    def initDictUI(self):
        self.setCentralWidget(DictWidget())

    def changeLanguage(self):
        pass
