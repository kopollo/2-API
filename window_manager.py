import sys

from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import (QApplication, QMainWindow, )

from api_ui import Ui_MainWindow
from config import GEOSEARCH_API_KEY, GEOCODER_API_KEY
from web_utils import generate_image, get_ll_by_address


MAP_TYPE = {'Scheme': 'map',
            'Sputnik': 'sat',
            'Hybrid': 'sat,skl'
            }

W, H = 600, 450


class Window(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.setWindowTitle('Андрей придумай название')
        self.scheme.nextCheckState()

        self.ll = '37.617698,55.755864'
        self.map_type = None
        self.place = None
        self.pt = None
        self.pixmap = QPixmap('./style/Yandex.jpg')
        self.z = 8

        self.buttonGroup.buttonClicked.connect(self.change_type_map)
        self.search.clicked.connect(self.take_parameters)
        self.show_image()

    def show_image(self):
        self.map.setPixmap(self.pixmap)

    def take_parameters(self):
        place = self.search_bar.text()
        self.map_type = MAP_TYPE[self.buttonGroup.checkedButton().text()]
        self.ll = get_ll_by_address(GEOCODER_API_KEY, place)
        self.pt = self.ll
        self.take_picture()

    def take_picture(self):
        # json = geosearch_request(apikey=GEOSEARCH_API_KEY, text=self.take_parameters())
        # generate_image(
        #     pt=self.pt, z=self.z, map_type=self.map_type, ll=self.ll
        # )
        generate_image(
            address_ll=self.ll,
            scale=self.z,
            map_type=self.map_type,
        )

        self.pixmap = QPixmap('map.png')
        self.show_image()

    def keyPressEvent(self, event):
        # use english layout
        # need to do it by value
        if event.key() in [Qt.Key_J, Qt.Key_L, Qt.Key_K, Qt.Key_I, Qt.Key_W, Qt.Key_S]:
            if event.key() == Qt.Key_W and self.z < 17:
                self.z += 1
            elif event.key() == Qt.Key_S and self.z > 0:
                self.z -= 1
            elif event.key() in [Qt.Key_J, Qt.Key_L, Qt.Key_K, Qt.Key_I]:
                longitude, latitude = [float(cord) for cord in self.ll.split(',')]
                if event.key() == Qt.Key_J:
                    longitude -= 360 / (2 ** (self.z + 8)) * W
                if event.key() == Qt.Key_L:
                    longitude += 360 / (2 ** (self.z + 8)) * W
                if event.key() == Qt.Key_K:
                    latitude -= 180 / (2 ** (self.z + 8)) * H
                if event.key() == Qt.Key_I:
                    latitude += 180 / (2 ** (self.z + 8)) * H
                self.ll = f'{longitude},{latitude}'
            self.take_picture()

    def change_type_map(self):
        self.map_type = MAP_TYPE[self.buttonGroup.checkedButton().text()]
        if self.pt is not None:
            self.take_picture()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    my_prog = Window()
    my_prog.show()
    sys.exit(app.exec())
