from PyQt5.QtWidgets import *

from View.widgets import IntroWidget, TrainWidget, DictWidget, callMsgBox
from PyQt5.QtGui import QIcon

class MainWindow(QMainWindow):
    def __init__(self, model):
        super().__init__()
        self.model = model
        self.initWindowFrame()
        self.initIntroWidget()
        self.setWindowTitle("DictTrainer")
        self.setGeometry(300, 300, 600, 600)
        self.show()
    # TODO TURN THIS SHIT ON
    def initWindowFrame(self):
        exitAction = QAction(QIcon('../Resources/exit.png'), self)
        exitAction.triggered.connect(qApp.quit)
        self.toolbar = self.addToolBar('Exit')
        self.toolbar.addAction(exitAction)


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
