import sys
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
import sys, os, time
from PyQt5.QtWidgets import QApplication, QWidget
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import QSize, Qt

pathname = os.path.dirname(os.path.realpath(__file__))
iconPath = os.path.join(pathname, 'img', 'icons', '78x23', 'load_n.jpg')

iconPath_78x23 = os.path.join(pathname, 'img', 'icons', '78x23', )
iconPath_24x23 = os.path.join(pathname, 'img', 'icons', '24x23', )
iconPath_main = os.path.join(pathname, 'img', 'icons', 'main', )

class tooldemo(QMainWindow):
    def __init__(self, parent=None):
        super(tooldemo, self).__init__(parent)
        layout = QVBoxLayout()
        tb = self.addToolBar("File")
        tb.setIconSize(QSize(78, 23))
        tb.setToolButtonStyle(Qt.ToolButtonIconOnly)

        new = QAction(QIcon("new.bmp"), "new", self)
        tb.addAction(new)

        open = QAction(QIcon("open.bmp"), "open", self)
        tb.addAction(open)
        save = QAction(QIcon("save.bmp"), "save", self)
        tb.addAction(save)
        tb.actionTriggered[QAction].connect(self.toolbtnpressed)
        self.setLayout(layout)
        self.setWindowTitle("toolbar demo")

    def toolbtnpressed(self, a):
        print
        "pressed tool button is", a.text()


def main():
    app = QApplication(sys.argv)
    ex = tooldemo()
    ex.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()