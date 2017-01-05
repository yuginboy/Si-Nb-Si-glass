#!/usr/bin/python3
# -*- coding: utf-8 -*-

"""
ZetCode PyQt5 tutorial

In this example, we create a simple
window in PyQt5.

author: Jan Bodnar
website: zetcode.com
last edited: January 2015
"""

import sys, os, time
from PyQt5.QtWidgets import QApplication, QWidget
from PyQt5.QtGui import QIcon

pathname = os.path.dirname(os.path.realpath(__file__))
iconPath = os.path.join(pathname, 'img', 'icons', '78x23', 'load_n.jpg')

iconPath_78x23 = os.path.join(pathname, 'img', 'icons', '78x23', )
iconPath_24x23 = os.path.join(pathname, 'img', 'icons', '24x23', )
iconPath_main = os.path.join(pathname, 'img', 'icons', 'main', )


from PyQt5.QtWidgets import (QWidget, QToolTip,
                             QPushButton, QApplication, QDesktopWidget, QGroupBox, QHBoxLayout, QMainWindow)
from PyQt5.QtGui import QFont


class Example(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setStyleSheet("background-color: #aeaaa7")
        self.initUI()
        self.form_widget = FormWidget(self)
        self.setCentralWidget(self.form_widget)
        # self.createHorizontalGroupBox()

    def initUI(self):
        QToolTip.setFont(QFont('SansSerif', 10))
        self.setToolTip('This is a <b>QWidget</b> widget')

        # btn = QPushButton( '', self)
        # btn.setToolTip('This is a <b>QPushButton</b> widget')
        # btn.resize(btn.sizeHint())
        # btn.setFixedSize(78, 23)
        # btn.setFlat(1)
        # btn.move(50, 50)
        #
        # icon = QIcon(iconPath)
        # btn.setStyleSheet("background-image: url(" + iconPath + ");")

        self.setGeometry(300, 300, 300, 200)
        self.setWindowTitle('Tooltips')
        self.show()

    def createHorizontalGroupBox(self):
        self.horizontalGroupBox = QGroupBox("Horizontal layout")
        layout = QHBoxLayout()

        for i in range(3):
            button = QPushButton("Button %d" % (i + 1))
            layout.addWidget(button)

        self.horizontalGroupBox.setLayout(layout)

    def centered(self, width, height):
        w = 800
        h = 600
        self.setGeometry( (width-w)*0.5, (height-h)*0.5, w, h,)

class FormWidget(QWidget):

    def __init__(self, parent):
        super(FormWidget, self).__init__(parent)
        self.layout = QHBoxLayout(self)

        self.button1 = QPushButton("Button 1")
        self.layout.addWidget(self.button1)

        self.button2 = QPushButton("Button 2")
        self.layout.addWidget(self.button2)

        btn = QPushButton('')
        btn.setToolTip('This is a <b>QPushButton</b> widget')
        btn.resize(btn.sizeHint())
        btn.setFixedSize(78, 23)
        btn.setFlat(1)
        # btn.move(50, 50)
        btn.setStyleSheet("background-image: url(" + os.path.join(iconPath_78x23, 'load_n.jpg') + ");")
        self.layout.addWidget(btn)

        self.setLayout(self.layout)



if __name__ == '__main__':
    app = QApplication(sys.argv)
    screen_resolution = app.desktop().screenGeometry()
    width, height = screen_resolution.width(), screen_resolution.height()
    ex = Example()
    ex.centered(width, height)
    sys.exit(app.exec_())