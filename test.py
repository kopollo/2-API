import sys

from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import (QApplication, QMainWindow,)

from API import Ui_MainWindow


class Window(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.setWindowTitle('test')
        # self.pixmap = QPixmap(QFileDialog.getOpenFileName(
        #     self, 'Выбрать картинку', '',
        #     'Картинка (*.jpg);;Картинка (*.png);;Все файлы (*)'
        # )[0])
        self.pixmap = QPixmap('./pict/Australia.jpg')
        self.show_image()

    def show_image(self):
        self.map.setPixmap(self.pixmap)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    my_prog = Window()
    my_prog.show()
    sys.exit(app.exec())
