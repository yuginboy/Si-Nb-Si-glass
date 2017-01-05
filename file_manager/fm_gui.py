#!/usr/bin/env python
from file_manager.default_styles import styleQToolBarDefault
import sys, os, time, qdarkstyle
from PyQt5.QtCore import QDate, QFile, Qt, QTextStream, QSize, QObject, QTimer, QDir
from PyQt5.QtGui import (QFont, QIcon, QKeySequence, QTextCharFormat,
        QTextCursor, QTextTableFormat)
from PyQt5.QtPrintSupport import QPrintDialog, QPrinter
from PyQt5.QtWidgets import (QAction, QApplication, QDialog, QDockWidget, QAbstractItemView,
        QFileDialog, QListWidget, QMainWindow, QMessageBox, QTextEdit, QWidget, QToolButton, QVBoxLayout, QToolBar)
from PyQt5.QtWidgets import QFileSystemModel, QTreeView, QGroupBox, QHBoxLayout, QPushButton, QGridLayout, QSizePolicy, QLabel




import random
import matplotlib
# Make sure that we are using QT5
matplotlib.use('Qt5Agg')

from numpy import arange, sin, pi
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure


pathname = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
iconPath_78x23 = os.path.join(pathname, 'img', 'icons', '78x23', )
iconPath_24x23 = os.path.join(pathname, 'img', 'icons', '24x23', )
iconPath_main = os.path.join(pathname, 'img', 'icons', 'main', )
stylePath = os.path.join(pathname, 'styles', 'dn.qss', )

startDir = os.path.realpath(__file__)


class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.setMinimumWidth(800)
        self.setMinimumHeight(600)
        # self.setStyleSheet("""background: #aeaaa7;
        #  background-color: #aeaaa7;
        # QMenuBar::item {
        #  background: #aeaaa7;
        #  background-color: #aeaaa7;
        # }""")
        # self.createHorizontalGroupBox()

        self.loadStyleSheet()
        self.main_widget = QWidget(self)
        l = QVBoxLayout(self.main_widget)
        self.sc = MyStaticMplCanvas(self.main_widget, width=5, height=4, dpi=100)
        dc = MyDynamicMplCanvas(self.main_widget, width=5, height=4, dpi=100)
        l.addWidget(self.sc)
        l.addWidget(dc)

        self.main_widget.setFocus()
        # self.textEdit = QTextEdit()
        self.setCentralWidget(self.main_widget)
        # self.createHorizontalGroupBox()
        self.createActions()

        self.createMenus()

        self.createToolBars()
        self.createStatusBar()
        self.createDockWindows()

        self.setWindowTitle("D'N File Manager")


    def newLetter(self):
        self.textEdit.clear()

        cursor = self.textEdit.textCursor()
        cursor.movePosition(QTextCursor.Start)
        topFrame = cursor.currentFrame()
        topFrameFormat = topFrame.frameFormat()
        topFrameFormat.setPadding(16)
        topFrame.setFrameFormat(topFrameFormat)

        textFormat = QTextCharFormat()
        boldFormat = QTextCharFormat()
        boldFormat.setFontWeight(QFont.Bold)
        italicFormat = QTextCharFormat()
        italicFormat.setFontItalic(True)

        tableFormat = QTextTableFormat()
        tableFormat.setBorder(1)
        tableFormat.setCellPadding(16)
        tableFormat.setAlignment(Qt.AlignRight)
        cursor.insertTable(1, 1, tableFormat)
        cursor.insertText("The Firm", boldFormat)
        cursor.insertBlock()
        cursor.insertText("321 City Street", textFormat)
        cursor.insertBlock()
        cursor.insertText("Industry Park")
        cursor.insertBlock()
        cursor.insertText("Some Country")
        cursor.setPosition(topFrame.lastPosition())
        cursor.insertText(QDate.currentDate().toString("d MMMM yyyy"),
                textFormat)
        cursor.insertBlock()
        cursor.insertBlock()
        cursor.insertText("Dear ", textFormat)
        cursor.insertText("NAME", italicFormat)
        cursor.insertText(",", textFormat)
        for i in range(3):
            cursor.insertBlock()
        cursor.insertText("Yours sincerely,", textFormat)
        for i in range(3):
            cursor.insertBlock()
        cursor.insertText("The Boss", textFormat)
        cursor.insertBlock()
        cursor.insertText("ADDRESS", italicFormat)

    def print_(self):
        document = self.textEdit.document()
        printer = QPrinter()

        dlg = QPrintDialog(printer, self)
        if dlg.exec_() != QDialog.Accepted:
            return

        document.print_(printer)

        self.statusBar().showMessage("Ready", 2000)

    def save(self):
        filename, _ = QFileDialog.getSaveFileName(self,
                "Choose a file name", '.', "HTML (*.html *.htm)")
        if not filename:
            return

        file = QFile(filename)
        if not file.open(QFile.WriteOnly | QFile.Text):
            QMessageBox.warning(self, "Dock Widgets",
                    "Cannot write file %s:\n%s." % (filename, file.errorString()))
            return

        out = QTextStream(file)
        QApplication.setOverrideCursor(Qt.WaitCursor)
        out << self.textEdit.toHtml()
        QApplication.restoreOverrideCursor()

        self.statusBar().showMessage("Saved '%s'" % filename, 2000)

    def undo(self):
        document = self.textEdit.document()
        document.undo()

    def insertCustomer(self, customer):
        if not customer:
            return
        customerList = customer.split(', ')
        document = self.textEdit.document()
        cursor = document.find('NAME')
        if not cursor.isNull():
            cursor.beginEditBlock()
            cursor.insertText(customerList[0])
            oldcursor = cursor
            cursor = document.find('ADDRESS')
            if not cursor.isNull():
                for i in customerList[1:]:
                    cursor.insertBlock()
                    cursor.insertText(i)
                cursor.endEditBlock()
            else:
                oldcursor.endEditBlock()

    def addParagraph(self, paragraph):
        if not paragraph:
            return
        document = self.textEdit.document()
        cursor = document.find("Yours sincerely,")
        if cursor.isNull():
            return
        cursor.beginEditBlock()
        cursor.movePosition(QTextCursor.PreviousBlock, QTextCursor.MoveAnchor,
                2)
        cursor.insertBlock()
        cursor.insertText(paragraph)
        cursor.insertBlock()
        cursor.endEditBlock()

    def about(self):
        QMessageBox.about(self, "About D'N File Manager",
                "The <b>File Manager</b> shows spectra for the further data manipulation "
                "You can select file from the <b><i>Dir View</i></b> menu and immediately see  "
                "the data and then you can apply some data processing algorithms.")

    def updateGraphWindow(self):
        self.sc.update_figure()

    def createActions(self):
        # ---------- File:
        self.loadAct = QAction(QIcon(os.path.join(iconPath_78x23, 'load_n.jpg') ),"&Load",
                self, shortcut=QKeySequence.New,
                statusTip="Load work directory", triggered=self.about)

        self.exportAct = QAction(QIcon(os.path.join(iconPath_78x23, 'export_n.jpg')), "&Export",
                               self, shortcut=QKeySequence.New,
                               statusTip="Export data", triggered=self.about)

        self.exitAct = QAction(QIcon(os.path.join(iconPath_78x23, 'exit_n.jpg')), "&Export",
                                 self, shortcut=QKeySequence.New,
                                 statusTip="Exit", triggered=self.close)

        # ------- Processing:
        self.viewAllAct = QAction(QIcon(os.path.join(iconPath_24x23, 'view_all_n.jpg')), "View all", self,
                               shortcut=QKeySequence.Save,
                               statusTip="Fit data to the graph window", triggered=self.updateGraphWindow)
        self.autoscaleAct = QAction(QIcon(os.path.join(iconPath_24x23, 'autoscale_n.jpg')), "Autoscale", self,
                               shortcut=QKeySequence.Save,
                               statusTip="Autoscale mod is ON", triggered=self.about,)

        # self.autoscaleAct(self.aa)


        self.saveAct = QAction(QIcon(os.path.join(iconPath_24x23, 'view_all_n.jpg')), "&Save...", self,
                shortcut=QKeySequence.Save,
                statusTip="Save the current form letter", triggered=self.save)

        self.printAct = QAction(QIcon(':/images/print.png'), "&Print...", self,
                shortcut=QKeySequence.Print,
                statusTip="Print the current form letter",
                triggered=self.print_)

        self.undoAct = QAction(QIcon(':/images/undo.png'), "&Undo", self,
                shortcut=QKeySequence.Undo,
                statusTip="Undo the last editing action", triggered=self.undo)

        self.quitAct = QAction("&Quit", self, shortcut="Ctrl+Q",
                statusTip="Quit the application", triggered=self.close)

        self.aboutAct = QAction("&About", self,
                statusTip="Show the application's About box",
                triggered=self.about)

        self.aboutQtAct = QAction("About &Qt", self,
                statusTip="Show the Qt library's About box",
                triggered=QApplication.instance().aboutQt)

    def createMenus(self):
        self.setStyleSheet("""
                QMenuBar
                {
                    background-color: #aeaaa7;
                    color: rgb(23,23,23);
                }

                QMenuBar::item
                {
                    background: transparent;
                }

                QMenuBar::item:selected
                {
                    background: transparent;
                    border: 1px solid #aeaaa7;
                }

                QMenuBar::item:pressed
                {
                    border: 1px solid #76797C;
                    background-color: rgb(128,128,128);
                    color: #000;
                    margin-bottom:-1px;
                    padding-bottom:1px;
                }

                QMenu {
                    background-color: #aeaaa7;
                    color: rgb(23,23,23);
                    border: 1px solid #000;
                }

                QMenu::item::selected {
                    background-color: rgb(128,128,128);
                }
            """)
        self.fileMenu = self.menuBar().addMenu("&File")
        self.fileMenu.addAction(self.loadAct)
        self.fileMenu.addAction(self.saveAct)
        self.fileMenu.addAction(self.printAct)
        self.fileMenu.addSeparator()
        self.fileMenu.addAction(self.quitAct)


        self.editMenu = self.menuBar().addMenu("&Edit")
        self.editMenu.addAction(self.undoAct)

        self.viewMenu = self.menuBar().addMenu("&View")

        self.menuBar().addSeparator()

        self.helpMenu = self.menuBar().addMenu("&Help")
        self.helpMenu.addAction(self.aboutAct)
        self.helpMenu.addAction(self.aboutQtAct)

    def createToolBars(self):
        # self.toolBar = QToolBar(self)
        # self.toolBar.setStyleSheet('QToolBar{border:0px;}')
        #
        # self.addToolBar(Qt.ToolBarArea(Qt.TopToolBarArea), self.toolBar)

        # self.spacer = QWidget()
        # self.spacer.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        #
        # self.actionLeft = QAction(self)
        # self.actionLeft.setIcon(QIcon.fromTheme("media-seek-backward"))
        #
        # self.actionRight = QAction(self)
        # self.actionRight.setIcon(QIcon.fromTheme("media-seek-forward"))

        # self.toolBar.addAction(self.actionLeft)
        # self.toolBar.addWidget(self.spacer)
        # self.toolBar.addAction(self.actionRight)

        self.fileToolBar = self.addToolBar('Files')
        self.fileToolBar.addAction(self.loadAct)
        self.fileToolBar.addAction(self.exportAct)
        self.fileToolBar.addAction(self.exitAct)

        self.additionalButtonsGroup = FormWidget(self)
        self.fileToolBar.addWidget(self.additionalButtonsGroup)
        self.fileToolBar.setIconSize(QSize(78, 23))
        # self.fileToolBar.setFloatable(1)

        self.fileToolBar.setToolButtonStyle(Qt.ToolButtonIconOnly)
        # self.fileToolBar.setStyleSheet('QToolBar{border:0px;}')
        # self.fileToolBar.addAction(self.saveAct)
        # self.fileToolBar.addAction(self.printAct)

        self.editToolBar = self.addToolBar('Processing')
        self.editToolBar.setIconSize(QSize(24, 23))
        # self.editToolBar.setStyleSheet('QToolBar{border:0px;}')
        self.editToolBar.addAction(self.autoscaleAct)
        self.editToolBar.addAction(self.viewAllAct)


        self.fileToolBar.setStyleSheet(styleQToolBarDefault)
        self.editToolBar.setStyleSheet(styleQToolBarDefault)

    def createStatusBar(self):
        # self.statusBar().showMessage("Ready")
        self.statusBar().addWidget(QLabel("Ready"))

    def createDockWindows(self):
        dock = QDockWidget("Dir View", self)
        dock.setAllowedAreas(Qt.LeftDockWidgetArea | Qt.RightDockWidgetArea)
        # self.fileTree = QListWidget(dock)
        self.dirModel = QFileSystemModel()
        # self.model.setRootPath(QDir.currentPath())

        self.dirTreeView = DirViewMain(dock)



        self.dirTreeView.setAnimated(False)
        self.dirTreeView.setIndentation(20)
        self.dirTreeView.setSortingEnabled(True)

        self.dirTreeView.setWindowTitle("Dir View")
        # self.dirTreeView.doubleClicked.connect(self.dblclcLoadFile)

        # self.customerList = QListWidget(dock)
        # self.customerList.addItems((
        #     "John Doe, Harmony Enterprises, 12 Lakeside, Ambleton",
        #     "Jane Doe, Memorabilia, 23 Watersedge, Beaton",
        #     "Tammy Shea, Tiblanka, 38 Sea Views, Carlton",
        #     "Tim Sheen, Caraba Gifts, 48 Ocean Way, Deal",
        #     "Sol Harvey, Chicos Coffee, 53 New Springs, Eccleston",
        #     "Sally Hobart, Tiroli Tea, 67 Long River, Fedula"))
        # dock.setWidget(self.customerList)
        # self.addDockWidget(Qt.RightDockWidgetArea, dock)
        # self.viewMenu.addAction(dock.toggleViewAction())

        dock.setWidget(self.dirTreeView)
        self.addDockWidget(Qt.RightDockWidgetArea, dock)
        # self.viewMenu.addAction(dock.toggleViewAction())

        dock = QDockWidget("Data", self)
        self.paragraphsList = QListWidget(dock)
        self.paragraphsList.addItems((
            "Thank you for your payment which we have received today.",
            "Your order has been dispatched and should be with you within "
                "28 days.",
            "We have dispatched those items that were in stock. The rest of "
                "your order will be dispatched once all the remaining items "
                "have arrived at our warehouse. No additional shipping "
                "charges will be made.",
            ))
        dock.setWidget(self.paragraphsList)
        self.addDockWidget(Qt.RightDockWidgetArea, dock)
        # self.viewMenu.addAction(dock.toggleViewAction())

        # self.customerList.currentTextChanged.connect(self.insertCustomer)
        self.paragraphsList.currentTextChanged.connect(self.addParagraph)

    def dblclcLoadFile(self, signal):
        file_path = self.dirModel().filePath(signal)
        print(file_path)

    def loadStyleSheet(self):
        file = QFile(stylePath)
        file.open(QFile.ReadOnly)

        styleSheet = file.readAll()
        styleSheet = str(styleSheet, encoding='utf8')

        # self.ui.styleTextEdit.setPlainText(styleSheet)
        # QApplication.instance().setStyleSheet(styleSheet)
        QApplication.instance().setStyleSheet(qdarkstyle.load_stylesheet_pyqt5())
        # self.ui.applyButton.setEnabled(False)

class FormWidget(QWidget):

    def __init__(self, parent):
        super(FormWidget, self).__init__(parent)
        self.layout = QHBoxLayout(self)

        self.button1 = QPushButton("1")
        self.layout.addWidget(self.button1)

        self.button2 = QPushButton("2")
        self.layout.addWidget(self.button2)

        # btn = QPushButton('')
        # btn.setToolTip('This is a <b>QPushButton</b> widget')
        # btn.resize(btn.sizeHint())
        # btn.setFixedSize(78, 23)
        # btn.setFlat(1)
        # # btn.move(50, 50)
        # btn.setStyleSheet("background-image: url(" + os.path.join(iconPath_78x23, 'load_n.jpg') + ");")
        # self.layout.addWidget(btn)

        self.setLayout(self.layout)

class DirViewMain(QTreeView):
    def __init__(self, parent=None):
        QTreeView.__init__(self, parent)
        model = QFileSystemModel()
        model.setRootPath('C:\\')
        self.setModel(model)

        # Path
        rootindex = model.setRootPath(QDir.rootPath())
        # homeindex = model.index(QDir.homePath())
        homeindex = model.index('/home/yugin/VirtualboxShare/soft/CasaXPS/P_Piotrowski/Au-T/results/report/from_customer')
        #
        self.setRootIndex(rootindex)
        self.scrollTo(homeindex, QAbstractItemView.PositionAtTop)
        self.expand(homeindex)
        self.resizeColumnToContents(0)

        # connect the double Click action:
        self.doubleClicked.connect(self.loadFile)
        self.clicked.connect(self.readFile)

    def readFile(self, signal):
        file_path=self.model().filePath(signal)
        print(file_path)

    def loadFile(self, signal):
        file_path=self.model().filePath(signal)
        print('Load file: ', file_path)

    def keyPressEvent(self, event):
        # pass the event up the chain or we will eat the event
        QTreeView.keyPressEvent(self, event)
        if event.key() == Qt.Key_Up or Qt.Key_Down:
            print('up or down')
            index = self.selectedIndexes()[0]
            file_path=self.model().filePath(index)
            print('key_pressed', file_path)



class MyMplCanvas(FigureCanvas):
    """Ultimately, this is a QWidget (as well as a FigureCanvasAgg, etc.)."""

    def __init__(self, parent=None, width=5, height=4, dpi=100):
        fig = Figure(figsize=(width, height), dpi=dpi)
        self.axes = fig.add_subplot(111)
        # We want the axes cleared every time plot() is called
        self.axes.hold(False)

        self.compute_initial_figure()

        #
        FigureCanvas.__init__(self, fig)
        self.setParent(parent)

        FigureCanvas.setSizePolicy(self,
                                   QSizePolicy.Expanding,
                                   QSizePolicy.Expanding)
        FigureCanvas.updateGeometry(self)

    def compute_initial_figure(self):
        pass


class MyStaticMplCanvas(MyMplCanvas):
    """Simple canvas with a sine plot."""

    def compute_initial_figure(self):
        t = arange(0.0, 3.0, 0.01)
        s = sin(2*pi*t)
        self.axes.plot(t, s)
    def update_figure(self):
        # Build a list of 4 random integers between 0 and 10 (both inclusive)
        l = [random.randint(0, 10) for i in range(4)]

        self.axes.plot([0, 1, 2, 3], l, 'r')
        self.draw()


class MyDynamicMplCanvas(MyMplCanvas):
    """A canvas that updates itself every second with a new plot."""

    def __init__(self, *args, **kwargs):
        MyMplCanvas.__init__(self, *args, **kwargs)
        timer = QTimer(self)
        timer.timeout.connect(self.update_figure)
        timer.start(1000)

    def compute_initial_figure(self):
        self.axes.plot([0, 1, 2, 3], [1, 2, 0, 4], 'r')

    def update_figure(self):
        # Build a list of 4 random integers between 0 and 10 (both inclusive)
        l = [random.randint(0, 10) for i in range(4)]

        self.axes.plot([0, 1, 2, 3], l, 'r')
        self.draw()



if __name__ == '__main__':

    import sys

    app = QApplication(sys.argv)
    mainWin = MainWindow()
    mainWin.show()
    mainWin.move(app.desktop().screen().rect().center() - mainWin.rect().center())
    sys.exit(app.exec_())
