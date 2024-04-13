import sys
import sqlite3
from PyQt6.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget, QPushButton, QGroupBox, QDialog
from PyQt6.QtWidgets import QTableWidget, QHBoxLayout, QCalendarWidget, QTextBrowser, QLineEdit, QMessageBox
from PyQt6.QtWidgets import QFormLayout, QComboBox, QDialogButtonBox, QLabel, QGridLayout, QTableWidgetItem
from PyQt6.QtGui import QIcon, QPixmap
from PyQt6.QtCore import Qt
# from PyQt6.QtCore import Qt, QDate


class EventDialog(QDialog):
    def __init__(self, apprentices):
        super().__init__()

        self.setWindowTitle("Event hinzufügen")
        self.setWindowIcon(QIcon("icons/buttons/event.png"))
        self.apprentices = apprentices

        layout = QVBoxLayout()

        form_layout = QFormLayout()

        self.apprentice_combo = QComboBox()
        for apprentice in apprentices:
            self.apprentice_combo.addItem(apprentice)
        form_layout.addRow("Lehrling:", self.apprentice_combo)

        self.reason_edit = QLineEdit()
        form_layout.addRow("Grund:", self.reason_edit)

        self.date_picker = QCalendarWidget()
        form_layout.addRow("Datum:", self.date_picker)

        layout.addLayout(form_layout)

        buttons = QDialogButtonBox(QDialogButtonBox.StandardButton.Ok | QDialogButtonBox.StandardButton.Cancel)
        buttons.accepted.connect(self.accept)
        buttons.rejected.connect(self.reject)

        layout.addWidget(buttons)

        self.setLayout(layout)

    def selected_apprentice(self):
        return self.apprentice_combo.currentText()

    def selected_date(self):
        return self.date_picker.selectedDate().toString("yyyy-MM-dd")

class CalendarApp(QMainWindow):
    def __init__(self):
        super().__init__()

        def create_table():
            conn = sqlite3.connect('test.db')
            c = conn.cursor()
            c.execute('''CREATE TABLE IF NOT EXISTS Lehrlinge
                         (id INTEGER PRIMARY KEY,
                         Vorname TEXT,
                         Nachname TEXT,
                         Beruf TEXT,
                         Lehrjahr INTEGER)''')
            conn.commit()
            conn.close()
        create_table()

        self.setWindowTitle("Teamverwaltung")
        self.setGeometry(100, 100, 1280, 720)
        self.setWindowIcon(QIcon("icons/logo/logo.ico"))

        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)

        main_layout = QHBoxLayout()

        # Left side: Add apprentice Group Box and apprentice List
        left_layout = QVBoxLayout()

        apprentice_group_box = QGroupBox("Lehrlinge")
        apprentice_layout = QGridLayout()

        self.add_apprentice_button = QPushButton(QIcon("icons/buttons/new.ico"), "Hinzufügen")
        apprentice_layout.addWidget(self.add_apprentice_button, 0, 0)

        self.edit_apprentice_button = QPushButton(QIcon("icons/buttons/edit_apprentice.png"), "Bearbeiten")
        apprentice_layout.addWidget(self.edit_apprentice_button, 0, 1)

        self.remove_apprentice_button = QPushButton(QIcon("icons/buttons/delete.png"), "Löschen")
        apprentice_layout.addWidget(self.remove_apprentice_button, 0 ,2)

        # Input fields with labels
        apprentice_layout.addWidget(QLabel("Lehrjahr:"), 1, 0)
        self.year_edit = QLineEdit()
        apprentice_layout.addWidget(self.year_edit, 1, 1)

        apprentice_layout.addWidget(QLabel("Beruf:"), 2, 0)
        self.category_edit = QLineEdit()
        apprentice_layout.addWidget(self.category_edit, 2, 1)

        apprentice_layout.addWidget(QLabel("Vorname:"), 3, 0)
        self.first_name_edit = QLineEdit()
        apprentice_layout.addWidget(self.first_name_edit, 3, 1)

        apprentice_layout.addWidget(QLabel("Nachname:"), 4, 0)
        self.last_name_edit = QLineEdit()
        apprentice_layout.addWidget(self.last_name_edit, 4, 1)

        # Picture addition in the apprentice group box with specific size
        picture_label = QLabel()
        pixmap = QPixmap("icons/test.jpg")  # Update the path as necessary
        scaled_pixmap = pixmap.scaled(160, 160, Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation)
        picture_label.setPixmap(scaled_pixmap)
        apprentice_layout.addWidget(picture_label, 1, 2, 4, 1)  # Spanning 4 rows and 1 column

        apprentice_group_box.setLayout(apprentice_layout)
        left_layout.addWidget(apprentice_group_box)

        # Add a new widget for input fields and labels
        input_fields_widget = QWidget()
        input_fields_layout = QFormLayout()

        input_fields_widget.setLayout(input_fields_layout)
        left_layout.addWidget(input_fields_widget)

        self.apprentice_list = QTableWidget()
        left_layout.addWidget(self.apprentice_list)

        # Right side: Calendar, Buttons, Event Display
        right_layout = QVBoxLayout()

        self.calendar = QCalendarWidget()
        self.calendar.setVerticalHeaderFormat(QCalendarWidget.VerticalHeaderFormat.ISOWeekNumbers)
        self.calendar.setGridVisible(True)
        right_layout.addWidget(self.calendar)

        button_layout = QHBoxLayout()

        self.vacation_button = QPushButton(QIcon("icons/buttons/vacation.png"), "Urlaub")
        self.vacation_button.clicked.connect(lambda: self.open_event_dialog("Urlaub"))
        button_layout.addWidget(self.vacation_button)

        self.sick_button = QPushButton(QIcon("icons/buttons/sick.png"), "Krank / Arzt")
        self.sick_button.clicked.connect(lambda: self.open_event_dialog(self.open_event_dialog))
        button_layout.addWidget(self.sick_button)

        self.compensation_button = QPushButton(QIcon("icons/buttons/compensation.png"), "Zeitausgleich")
        self.compensation_button.clicked.connect(lambda: self.open_event_dialog("Zeitausgleich"))
        button_layout.addWidget(self.compensation_button)

        right_layout.addLayout(button_layout)

        button_layout_2 = QHBoxLayout()

        self.remove_event_button = QPushButton(QIcon("icons/buttons/delete_event.png"), "Eintrag löschen")
        self.remove_event_button.clicked.connect(lambda: self.open_event_dialog("Eintrag löschen"))
        button_layout_2.addWidget(self.remove_event_button)

        self.edit_event_button = QPushButton(QIcon("icons/buttons/edit.png"), "Eintrag bearbeiten")
        self.edit_event_button.clicked.connect(lambda: self.open_event_dialog("Eintrag bearbeiten"))
        button_layout_2.addWidget(self.edit_event_button)

        right_layout.addLayout(button_layout_2)

        self.event_display = QTextBrowser()
        right_layout.addWidget(self.event_display)

        # Add left and right layouts to the main layout
        main_layout.addLayout(left_layout)
        main_layout.addLayout(right_layout)

        self.central_widget.setLayout(main_layout)

        self.events = []
        self.apprentices = []

        # Connect the clicked signal of the calendar to the update_event_display slot
        self.calendar.clicked.connect(self.update_event_display)

    def open_event_dialog(self, event_type):
        dialog = EventDialog(self.apprentices)
        if dialog.exec() == QDialog.DialogCode.Accepted:
            apprentice = dialog.selected_apprentice()
            date = dialog.selected_date()
            self.add_event(event_type, apprentice, date)

    def add_event(self, event_type, apprentice, date):
        event = {"event_type": event_type, "apprentice": apprentice, "date": date}
        self.events.append(event)
        QMessageBox.information(self, "Erfolg", "Ereignis erfolgreich hinzugefügt!")
        self.update_event_display()

    def update_event_display(self):
        self.event_display.clear()
        selected_date = self.calendar.selectedDate().toString("yyyy-MM-dd")
        events_on_date = [event for event in self.events if event["date"] == selected_date]
        if events_on_date:
            self.event_display.append(f"Ereignisse für {selected_date}:")
            for event in events_on_date:
                self.event_display.append(f"- {event['event_type']} : {event['apprentice']}")
        else:
            self.event_display.append(f"Keine Ereignisse für {selected_date}")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = CalendarApp()
    window.show()
    sys.exit(app.exec())
