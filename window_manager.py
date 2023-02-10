import sys

from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import (QApplication, QMainWindow, )

from api_ui import Ui_MainWindow
from config import GEOSEARCH_API_KEY
from web_utils import geosearch_request, generate_image


class Window(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.setWindowTitle('test')
        self.pixmap = QPixmap('./pict/Yandex.jpg')
        self.show_image()
        self.search.clicked.connect(self.take_picture)
        self.z = 8

    def show_image(self):
        self.map.setPixmap(self.pixmap)

    def take_picture(self):
        json = geosearch_request(apikey=GEOSEARCH_API_KEY, text=self.search_bar.text())
        generate_image(json, z=self.z)
        self.pixmap = QPixmap('map.png')
        self.show_image()

    def keyPressEvent(self, event):
        # use english layout
        # need to do it by value
        if event.key() == Qt.Key_W:
            if self.z < 17:
                self.z += 1
                self.take_picture()
        if event.key() == Qt.Key_S:
            if self.z > 0:
                self.z -= 1
                self.take_picture()
        if event.key() == Qt.Key_Left:
            pass
        if event.key() == Qt.Key_Up:
            pass
        if event.key() == Qt.Key_Right:
            pass
        if event.key() == Qt.Key_Down:
            pass


if __name__ == '__main__':
    app = QApplication(sys.argv)
    my_prog = Window()
    my_prog.show()
    sys.exit(app.exec())
