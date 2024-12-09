from ui.calender_config import CalenderApp
from PyQt6.QtWidgets import QApplication

if __name__ == "__main__":
    import sys
    import qdarktheme # type: ignore
    app = QApplication(sys.argv)
    

    window = CalenderApp()
    window.show()
    sys.exit(app.exec())
    # Apply the dark theme stylesheet
    #TODO: let user choose which mode is default with database
    app.setStyleSheet(qdarktheme.load_stylesheet("light"))