from PySide2 import QtWidgets
from PySide2 import QtCore
from PySide2 import QtGui
from ui import main
import os

# window class,
class MyQtApp(main.Ui_MainWindow, QtWidgets.QMainWindow):
    def __init__(self):
        # set up the window
        super(MyQtApp, self).__init__()
        self.setupUi(self)

        # use custom contex menu and set the custom context menu
        self.treeView.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
        self.treeView.customContextMenuRequested.connect(self.context_menu)

        self.populate_treeView()

    def populate_treeView(self):
        path = 'C:/Windows'

        # create file system model
        self.fileSysModel = QtWidgets.QFileSystemModel()
        self.fileSysModel.setRootPath(QtCore.QDir.rootPath())

        # set treeview model to new created file system model
        self.treeView.setModel(self.fileSysModel)

        #limit the root to defined root
        self.treeView.setRootIndex(self.fileSysModel.index(path))

        #enable sort
        self.treeView.setSortingEnabled(True)



    def context_menu(self):
        menu = QtWidgets.QMenu()
        openAction = menu.addAction("Open")
        openAction.triggered.connect(self.open_file)

        # menu position
        cursor = QtGui.QCursor()
        menu.exec_(cursor.pos())

    def open_file(self):
        # get current file path
        index = self.treeView.currentIndex()
        fil_path = self.fileSysModel.filePath(index)
        os.startfile(fil_path)
        print (fil_path)

if __name__=='__main__':
    # Qapplication , can have only 1 in the program
    app = QtWidgets.QApplication()
    at_app = MyQtApp()
    at_app.show()
    app.exec_()