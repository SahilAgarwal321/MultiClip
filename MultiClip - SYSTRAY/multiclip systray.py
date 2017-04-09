'''
Runs within the system tray -
- Looks at a given folder (mc_dir) and creates a nested contexton right-click.
- Nested menu will show all folders/files within the parent directory.
- Selecting a folder opens a new nested menu for that folder.
- Selecting a file copies the file contents to the clipboard.
'''

import sys, os, pyperclip
from PyQt5 import QtCore, QtGui, QtWidgets

mc_dir = "D:\\Python\\MC\\"
systray_icon = "D:\\Python\\mc.ico"


class SystemTrayIcon(QtWidgets.QSystemTrayIcon):

    def __init__(self, icon, parent=None):
        QtWidgets.QSystemTrayIcon.__init__(self, icon, parent)
        menu = QtWidgets.QMenu(parent)

        self.list_subfolders(mc_dir, menu)
        self.setContextMenu(menu)
        menu.addSeparator()
        self.create_exit(menu)

    def create_exit(self, menu):
        '''
            Creates exit option in menu.
        '''
        exitAction = menu.addAction("Exit")
        exitAction.triggered.connect(self.close)

    def close(self):
        '''
            Call to exit the program
        '''
        exit()

    def list_subfolders(self, path, menu):
        '''
            Detects subfolders, calls file lister for main folder.
            Recursively calls itself for subfolders.
        '''
        for i in os.listdir(path):
            object_path = path +'/'+ i
            if os.path.isdir(object_path) is True:
                subfolder_menu = self.create_submenu(i, menu)
                self.list_subfolders(object_path, subfolder_menu)
        self.list_files(path, menu)

    def list_files(self, path, menu):
        '''
        Lists files in the folder.
        '''
        for i in os.listdir(path):
            object_path = path +'/'+ i
            if os.path.isfile(object_path) is True:
                self.create_file_in_menu(object_path, menu) # changed "i" to object_path
                # changed due to an issue with opening the file, when using "i" - unable to open the file to copy
                # when clicked, will need to find new solution as it is not feasible to have full filepath for each item
                # even though with "i" it is being detected that "namehere.txt" is being clicked, unable to find/open file
    
    def create_submenu(self, i, menu):
        '''
        Create submenu in the menu for subfolder.
        '''
        subfolder_menu = menu.addMenu(i)
        return subfolder_menu

    def create_file_in_menu(self, i, menu):
        '''
        Create file in the menu.
        '''
        file_menu = menu.addAction(i)
        file_menu.triggered.connect(self.copy_contents)

    def copy_contents(self):
        '''
        Copies the selected files contents to clipboard.
        '''
        snd = self.sender().text()
        txt_to_copy = open((snd), "r").read()
        pyperclip.copy(txt_to_copy)

def main(image):
    app = QtWidgets.QApplication(sys.argv)

    w = QtWidgets.QWidget()
    trayIcon = SystemTrayIcon(QtGui.QIcon(image), w)

    trayIcon.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    on = systray_icon
main(on)
