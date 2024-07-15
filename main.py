from ui.calender_config import CalenderApp
from PyQt6.QtWidgets import QApplication


if __name__ == "__main__":
    import sys

    # standard application
    app = QApplication(sys.argv)
    window = CalenderApp()
    window.show()
    sys.exit(app.exec())