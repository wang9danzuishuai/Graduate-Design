from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QMainWindow
from recog_panel import Ui_MainWindow


class Main_UI(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)


if __name__ == '__main__':
    app = QtWidgets.QApplication([])
    main_ui = Main_UI()
    main_ui.show()
    app.exec_()