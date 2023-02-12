import sys

from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import (QApplication, QMainWindow, )

from api_ui import Ui_MainWindow
from config import GEOSEARCH_API_KEY, GEOCODER_API_KEY
from web_utils import generate_image, get_ll_by_address


class Geofinder(QMainWindow, Ui_MainWindow):
    BASE_SCALE = 17
    MAP_TYPE = {
        'Scheme': 'map',
        'Sputnik': 'sat',
        'Hybrid': 'sat,skl'
    }
    KEYBOARD_KEYS = [
        Qt.Key_J, Qt.Key_L, Qt.Key_K, Qt.Key_I, Qt.Key_W,
        Qt.Key_S,
    ]

    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.setWindowTitle('Geofinder')
        self.scheme.nextCheckState()

        self.map_type = Geofinder.MAP_TYPE['Scheme']
        self.org_name = None
        self.center_point = None
        self.pixmap = QPixmap('./style/Yandex.jpg')
        self.scale = Geofinder.BASE_SCALE

        self.buttonGroup.buttonClicked.connect(self.change_type_map)
        self.search.clicked.connect(self._search_btn_clicked)
        self.show_image()

        self.search_bar.setText('гум')

    def show_image(self):
        self.map.setPixmap(self.pixmap)

    def _search_btn_clicked(self):
        self.scale = Geofinder.BASE_SCALE
        self.org_name = self.search_bar.text()
        self.org_point = get_ll_by_address(
            key=GEOSEARCH_API_KEY,
            address=self.org_name
        )
        self.center_point = self.org_point
        self.take_picture()

    def take_picture(self):
        generate_image(
            center_point=self.center_point,
            org_point=self.org_point,
            map_type=self.map_type,
            scale=self.scale,
        )
        self.pixmap = QPixmap('map.png')
        self.show_image()

    def keyPressEvent(self, event):
        W, H = 600, 450
        if event.key() == Qt.Key_W and self.scale < 17:
            self.scale += 1
        elif event.key() == Qt.Key_S and self.scale > 0:
            self.scale -= 1
        elif event.key() in [Qt.Key_J, Qt.Key_L, Qt.Key_K, Qt.Key_I]:
            longitude, latitude = [float(cord) for cord in
                                   self.center_point.split(',')]
            if event.key() == Qt.Key_J:
                longitude -= 360 / (2 ** (self.scale + 8)) * W
            if event.key() == Qt.Key_L:
                longitude += 360 / (2 ** (self.scale + 8)) * W
            if event.key() == Qt.Key_K:
                latitude -= 180 / (2 ** (self.scale + 8)) * H
            if event.key() == Qt.Key_I:
                latitude += 180 / (2 ** (self.scale + 8)) * H
            self.center_point = f'{longitude},{latitude}'
        if event.key() in Geofinder.KEYBOARD_KEYS:
            self.take_picture()

    def change_type_map(self):
        self.map_type = Geofinder.MAP_TYPE[
            self.buttonGroup.checkedButton().text()]
        self.take_picture()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    geofinder = Geofinder()
    geofinder.show()
    sys.exit(app.exec())
