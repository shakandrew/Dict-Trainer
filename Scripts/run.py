import sys

from PyQt5.QtWidgets import QApplication
from View.mainwindow import MainWindow
from Model.model import Model

def main():
    app = QApplication(sys.argv)
    window = MainWindow(Model())
    sys.exit(app.exec_())

if __name__=="__main__":
    main()