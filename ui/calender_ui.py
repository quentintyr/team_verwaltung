from PyQt6 import QtWidgets, uic
from PyQt6.QtGui import QIcon

class CalenderApp(QtWidgets.QMainWindow):
    def __init__(self):
        super(CalenderApp, self).__init__()   # call the inherited classes __init__ method
        uic.loadUi('ui/calender_ui.ui', self)   # load the ui file
        self.show()

        # main window settings
        self.setWindowTitle("World Backups")
        self.setWindowIcon(QIcon("icons/logo_rect.png"))