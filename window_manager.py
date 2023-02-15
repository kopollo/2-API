import sys

from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import (QApplication, QMainWindow, )

import web_utils
from api_ui import Ui_MainWindow
from config import GEOSEARCH_API_KEY, GEOCODER_API_KEY
from web_utils import generate_image, geosearch_controller


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
        self.org_point = geosearch_controller.get_ll_by_address(
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
        self.address.setText(self.get_full_address())

    def get_full_address(self):
        return web_utils.geosearch_controller.get_full_address(
            address=self.org_name
        )

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_W:
            self.scale += 1
        elif event.key() == Qt.Key_S:
            self.scale -= 1
        elif event.key() in [Qt.Key_J, Qt.Key_L, Qt.Key_K, Qt.Key_I]:
            self.update_center_point(event)

        if event.key() in Geofinder.KEYBOARD_KEYS:
            self.scale_checker()
            self.take_picture()

    def update_center_point(self, event):
        longitude, latitude = [float(cord) for cord in
                               self.center_point.split(',')]
        if event.key() == Qt.Key_J:
            if longitude - self.count_longitude() > -180:
                longitude -= self.count_longitude()
        if event.key() == Qt.Key_L:
            if longitude + self.count_longitude() < 180:
                longitude += self.count_longitude()
        if event.key() == Qt.Key_K:
            if latitude - self.count_latitude() > -90:
                latitude -= self.count_latitude()
        if event.key() == Qt.Key_I:
            if latitude + self.count_latitude() < 90:
                latitude += self.count_latitude()
        self.center_point = f'{longitude},{latitude}'

    def scale_checker(self):
        self.scale = min(self.scale, 17)
        self.scale = max(self.scale, 0)

    def count_latitude(self):
        H = 450
        return 180 / (2 ** (self.scale + 8)) * H

    def count_longitude(self):
        W = 600
        return 360 / (2 ** (self.scale + 8)) * W

    def change_type_map(self):
        self.map_type = Geofinder.MAP_TYPE[
            self.buttonGroup.checkedButton().text()]
        if self.org_name:
            self.take_picture()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    geofinder = Geofinder()
    geofinder.show()
    sys.exit(app.exec())
