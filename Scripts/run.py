import sys

from PyQt5.QtWidgets import QApplication

from Model.model import Model
from View.mainwindow import MainWindow


def main():
    app = QApplication(sys.argv)
    window = MainWindow(Model())
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
