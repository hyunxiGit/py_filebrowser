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
        path = r'C:\MyGit\MayaTestScene'

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
        open_action = menu.addAction("Open in maya")
        open_action.triggered.connect(lambda : self.maya_file_operation(open_file=True))

        import_maya_action = menu.addAction("import to Maya")
        import_maya_action.triggered.connect(lambda : self.maya_file_operation(reference=True))

        # menu position
        cursor = QtGui.QCursor()
        menu.exec_(cursor.pos())

    def open_file(self):
        # get current file path
        index = self.treeView.currentIndex()
        fil_path = self.fileSysModel.filePath(index)
        os.startfile(fil_path)
        print (fil_path)

    def maya_file_operation(self,reference = False, open_file = False):
        print ('maya_file_operation')
        import maya.cmds as cmds
        index = self.treeView.currentIndex()
        file_path = self.fileSysModel.filePath(index)
        if reference :
            cmds.file(file_path, reference = True, type ='mayaAscii' , groupReference = True)
        elif open_file:
            # cmds.file(file_path,reference = True, type = 'mayaAscii' , groupReference = True)
            # get current file path
            file_location = cmds.file(query=True, location=True)
            # if current file is tmp file and not saved
            if file_location == 'unknown':
                cmds.file(file_path, open=True, force=True)
            else:
                # check if current file is modifies
                modify_file = cmds.file(query=True, modified=True)
                if modify_file:
                    # if file changed create window with btns to save or not save
                    # save the clicked yes/no tp result
                    result = cmds.confirmDialog(title='Opening new maya file',
                                                message='Current file is modified. Do you wan to save this file?',
                                                button=['yes', 'no'], defaultButton='yes', cancelButton='no',
                                                dismissString='no')
                    if result == 'yes':
                        # save file
                        cmds.file(save=True, type='mayaAscii')
                        # open the selected file
                        cmds.file(file_path, open=True, force=True)
                    else:
                        cmds.file(file_path, open=True, force=True)
                else:
                    cmds.file(file_path, open=True, force=True)


if __name__=='__main__':
    # Qapplication , can have only 1 in the program
    app = QtWidgets.QApplication()
    at_app = MyQtApp()
    at_app.show()
    app.exec_()