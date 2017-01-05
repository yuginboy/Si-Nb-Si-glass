'''
* Created by Zhenia Syryanyy (Yevgen Syryanyy)
* e-mail: yuginboy@gmail.com
* License: this code is in GPL license
* Last modified: 2016-10-08
'''
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QTreeView, QFileSystemModel, QApplication, QColumnView, QDockWidget, QMainWindow, QTextEdit
from PyQt5.QtCore import QDir, Qt

rootpath = QDir.currentPath()

class Browser(QMainWindow):
    def __init__(self):
        super(Browser, self).__init__()
        self.createDockWindows()
        self.textEdit = QTextEdit()
        self.setCentralWidget(self.textEdit)
    def createDockWindows(self):
        dock = QDockWidget("Folders", self)
        dock.setAllowedAreas(Qt.LeftDockWidgetArea | Qt.RightDockWidgetArea)
        #Code to Create FileView Colums and FolderTree
        self.FileView = QtWidgets.QColumnView()
        self.FileView.setGeometry(QtCore.QRect(240, 10, 291, 281))
        self.FolderTree = QtWidgets.QTreeView()
        self.FolderTree.setGeometry(QtCore.QRect(10, 10, 221, 281))
        FolderTree = self.FolderTree
        #FolderTree.hidecolumn(1),... ?? to show only name column

        #include FolderTree to a Dock at the left side
        dock.setWidget(FolderTree)
        self.addDockWidget(Qt.LeftDockWidgetArea, dock)
        #set the model and rootpath for filling the FolderTree from self.ui
        dirmodel = QFileSystemModel()
        #set filter to show only folders
        dirmodel.setFilter(QDir.NoDotAndDotDot | QDir.AllDirs)
        dirmodel.setRootPath(rootpath)
        #filemodel and filter for only files on right side
        filemodel = QFileSystemModel()
        filemodel.setFilter(QDir.NoDotAndDotDot | QDir.Files)
        filemodel.setRootPath(rootpath)
        FolderView = self.FolderTree
        FolderView.setModel(dirmodel)
        FolderView.setRootIndex(dirmodel.index(rootpath))
        FileView = self.FileView
        FileView.setModel(filemodel)
        FileView.setRootIndex(filemodel.index(rootpath))
        dock = QDockWidget("Files", self)
        dock.setWidget(FileView)
        self.addDockWidget(Qt.RightDockWidgetArea, dock)

        #important lines for the connection, which does not work
        self.FolderTree.clicked['QModelIndex'].connect(self.setpathonclick)
    def setpathonclick(self, index):
        rootpath = self.FolderTree.model().filePath(index)
        filemodel = self.FileView.model()
        filemodel.setRootPath(rootpath)
        self.FileView.setRootIndex(filemodel.index(rootpath))

        # currentpathindex = self.FolderTree.currentIndex()
        # self.FileView.setCurrentIndex(currentpathindex)

if __name__ == '__main__':
    import sys
    app = QApplication(sys.argv)
    w = Browser()
    w.resize(640, 480)
    w.show()
    sys.exit(app.exec_())