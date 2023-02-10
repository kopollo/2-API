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
        
    def eventFilter(self, obj, e):
        if obj == self.image and e.type() == 2:
            temp = list(map(int, str(e.pos()).split('(')[1][:-1].split(',')))
            print(temp)
            self.searchByOrganization(temp)
        return super(QMainWindow, self).eventFilter(obj, e)
    
    def keyPressEvent(self, event):
        if event.key() == Qt.Key_PageUp:
            try:
                self.mashtab.setPlainText(str(float(self.mashtab.toPlainText()) + 0.01))
                self.setImageToPixmap()
            except FloatingPointError as e:
                print(e)
        if event.key() == Qt.Key_PageDown:
            try:
                self.mashtab.setPlainText(str(float(self.mashtab.toPlainText()) - 0.01))
                self.setImageToPixmap()
            except FloatingPointError as e:
                print(e)
        if event.key() == Qt.Key_Up:
            try:
                self.edit_y.setPlainText(str(float(self.edit_y.toPlainText()) + (1 / 2) * float(self.mashtab.toPlainText())))
                self.setImageToPixmap()
            except FloatingPointError as e:
                print(e)
        if event.key() == Qt.Key_Down:
            try:
                self.edit_y.setPlainText(str(float(self.edit_y.toPlainText()) - (1 / 2) * float(self.mashtab.toPlainText())))
                self.setImageToPixmap()
            except FloatingPointError as e:
                print(e)
        if event.key() == Qt.Key_Right:
            try:
                self.edit_x.setPlainText(str(float(self.edit_x.toPlainText()) + 1 * float(self.mashtab.toPlainText())))
                self.setImageToPixmap()
            except FloatingPointError as e:
                print(e)
        if event.key() == Qt.Key_Left:
            try:
                self.edit_x.setPlainText(str(float(self.edit_x.toPlainText()) - 1 * float(self.mashtab.toPlainText())))
                self.setImageToPixmap()
            except FloatingPointError as e:
                print(e)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    my_prog = Window()
    my_prog.show()
    sys.exit(app.exec())
