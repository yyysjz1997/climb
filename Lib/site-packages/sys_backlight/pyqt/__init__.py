#! /usr/bin/env python3

"""
Program to change display brightness from commandline
"""

# internal imports
import sys_backlight
from .. import backlight

import sys
from PyQt5.QtCore import pyqtSignal, Qt
from PyQt5.QtWidgets import (QApplication, QBoxLayout, QGroupBox, QHBoxLayout, QSlider, QStackedWidget, QWidget)

class SlidersGroup(QGroupBox):

    valueChanged = pyqtSignal(int)

    def __init__(self, orientation, title, parent=None):
        super(SlidersGroup, self).__init__(title, parent)

        self.slider = QSlider(orientation)
        self.slider.setFocusPolicy(Qt.StrongFocus)
        self.slider.setTickPosition(QSlider.TicksBothSides)
        self.slider.setTickInterval(10)
        self.slider.setSingleStep(1)
        self.slider.setMinimum(0)
        self.slider.setMaximum(100)
        self.slider.setFixedWidth(400)

        self.slider.setValue(backlight.Backlight().getrel())

        self.slider.valueChanged[int].connect(self.changeBrightness)

        direction = QBoxLayout.TopToBottom

        slidersLayout = QBoxLayout(direction)
        slidersLayout.addWidget(self.slider)
        self.setLayout(slidersLayout)

    def setValue(self, value):
        self.slider.setValue(value)

    def changeBrightness(self, value):
        b = backlight.Backlight()
        b.setrel(value)

class Window(QWidget):
    def __init__(self):
        super(Window, self).__init__()

        self.setWindowTitle("sys_backlight")

        self.horizontalSliders = SlidersGroup(Qt.Horizontal,"Screen brightness")

        self.stackedWidget = QStackedWidget()
        self.stackedWidget.addWidget(self.horizontalSliders)

        layout = QHBoxLayout()
        layout.addWidget(self.stackedWidget)
        self.setLayout(layout)

def main():
    app = QApplication(sys.argv)
    window = Window()
    window.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
