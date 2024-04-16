import sys
import sqlite3
import PyQt6.QtCore
from PyQt6.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget, QPushButton, QGroupBox, QDialog
from PyQt6.QtWidgets import QTableWidget, QHBoxLayout, QCalendarWidget, QTextBrowser, QLineEdit, QMessageBox
from PyQt6.QtWidgets import QFormLayout, QComboBox, QDialogButtonBox, QLabel, QGridLayout, QTableWidgetItem
from PyQt6.QtGui import QIcon, QPixmap
from PyQt6.QtCore import Qt
from PyQt6.QtCore import QDate


class CalendarApp(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Teamverwaltung")  # creating the window
        self.setGeometry(100, 100, 1280, 720)
        self.setWindowIcon(QIcon("icons/logo/logo.ico"))

        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)

        main_layout = QHBoxLayout()  # creating the main layout
        left_layout = QVBoxLayout()  # left side: Add apprentice Group Box and apprentice List

        apprentice_group_box = QGroupBox("Lehrlinge")  # creating the group box and layout
        apprentice_layout = QGridLayout()

        # creating the buttons and setting the position in the grid layout
        self.add_apprentice_button = QPushButton(QIcon("icons/buttons/new.ico"), "Hinzufügen")  # add button
        apprentice_layout.addWidget(self.add_apprentice_button, 0, 0)

        self.edit_apprentice_button = QPushButton(QIcon("icons/buttons/save.png"), "Bearbeiten / Speichern")
        self.edit_apprentice_button.clicked.connect(self.save_apprentice_changes)  # edit button
        apprentice_layout.addWidget(self.edit_apprentice_button, 0, 1)

        self.remove_apprentice_button = QPushButton(QIcon("icons/buttons/delete.png"), "Löschen")  # delete button
        apprentice_layout.addWidget(self.remove_apprentice_button, 0, 2)

        apprentice_layout.addWidget(QLabel("Lehrjahr:"), 1, 0)  # input fields with labels
        self.year_edit = QLineEdit()
        apprentice_layout.addWidget(self.year_edit, 1, 1)

        apprentice_layout.addWidget(QLabel("Zeitausgleich:"), 1, 2)  # time compensation label and field
        self.za_edit = QLineEdit()
        apprentice_layout.addWidget(self.za_edit, 2, 2)

        apprentice_layout.addWidget(QLabel("Beruf:"), 2, 0)  # profession label and field
        self.category_edit = QLineEdit()
        apprentice_layout.addWidget(self.category_edit, 2, 1)

        apprentice_layout.addWidget(QLabel("Vorname:"), 3, 0) # first_name label and field
        self.first_name_edit = QLineEdit()
        apprentice_layout.addWidget(self.first_name_edit, 3, 1)

        apprentice_layout.addWidget(QLabel("Urlaub:"), 3, 2)  # vacation field and label
        self.vacation_edit = QLineEdit()
        apprentice_layout.addWidget(self.vacation_edit, 4, 2)

        apprentice_layout.addWidget(QLabel("Nachname:"), 4, 0)  # last name field and label
        self.last_name_edit = QLineEdit()
        apprentice_layout.addWidget(self.last_name_edit, 4, 1)

        apprentice_group_box.setLayout(apprentice_layout)  # apprentice group box
        left_layout.addWidget(apprentice_group_box)

        table_group_box = QGroupBox("Tabelle")  # table group box
        table_layout = QGridLayout()

        self.search_apprentice_button = QPushButton(QIcon("icons/buttons/search.png"), "Suchen")
        self.search_apprentice_button.setFixedWidth(113)  # search button and search field
        table_layout.addWidget(self.search_apprentice_button, 0, 0, 0, 5)
        self.search_field = QLineEdit()
        self.search_field.setFixedWidth(200)
        table_layout.addWidget(self.search_field, 0, 1, 0, 0)

        table_group_box.setLayout(table_layout)  # table group box
        left_layout.addWidget(table_group_box)

        self.apprentice_list = QTableWidget()  # apprentice list table widget
        self.apprentice_list.itemClicked.connect(self.update_input_fields_from_table)
        left_layout.addWidget(self.apprentice_list)

        right_layout = QVBoxLayout()  # right side: Calendar, Buttons, Event Display

        self.calendar = QCalendarWidget()  # calender widget
        self.calendar.setVerticalHeaderFormat(QCalendarWidget.VerticalHeaderFormat.ISOWeekNumbers)
        self.calendar.setGridVisible(True)
        right_layout.addWidget(self.calendar)

        button_layout = QHBoxLayout()  # buttons layout

        self.vacation_button = QPushButton(QIcon("icons/buttons/vacation.png"), "Urlaub")  # vacation button
        button_layout.addWidget(self.vacation_button)

        self.sick_button = QPushButton(QIcon("icons/buttons/sick.png"), "Krank / Arzt")  # sick button
        button_layout.addWidget(self.sick_button)

        self.compensation_button = QPushButton(QIcon("icons/buttons/compensation.png"), "Zeitausgleich")
        button_layout.addWidget(self.compensation_button)  # time compensation button

        self.school_button = QPushButton(QIcon("icons/buttons/vacation.png"), "Berufsschule")  # school button
        button_layout.addWidget(self.school_button)

        right_layout.addLayout(button_layout)  # adding the event button layout to the right layout

        entry_button_layout = QHBoxLayout()  # event layout

        self.remove_event_button = QPushButton(QIcon("icons/buttons/delete_event.png"), "Eintrag löschen")
        entry_button_layout.addWidget(self.remove_event_button)  # remove entry button

        self.edit_event_button = QPushButton(QIcon("icons/buttons/edit.png"), "Eintrag bearbeiten")
        entry_button_layout.addWidget(self.edit_event_button)  # edit entry button

        right_layout.addLayout(entry_button_layout)  # adding the entry button layout to the right layout

        self.event_display = QTextBrowser()  # adding the entry display
        right_layout.addWidget(self.event_display)

        main_layout.addLayout(left_layout)  # add left and right layouts to the main layout
        main_layout.addLayout(right_layout)

        self.central_widget.setLayout(main_layout)

        self.events = []
        self.apprentices = []

        self.load_apprentices_from_database()  # Load apprentices from database
        self.update_event_display()  # Update the event display widget

        # Connect the clicked signal of the calendar to the update_event_display slot
        self.calendar.clicked.connect(self.update_event_display)

    def load_apprentices_from_database(self):
        conn = sqlite3.connect('apprentices.db')
        c = conn.cursor()
        c.execute("SELECT profession, year, first_name, last_name, za, vacation "
                  "FROM Lehrlinge ORDER BY year, profession, last_name")
        self.apprentices = c.fetchall()
        conn.close()

        self.apprentice_list.setColumnCount(6)   # populate the table widget with fetched data
        self.apprentice_list.setHorizontalHeaderLabels(["Beruf", "Lehrjahr", "Vorname", "Nachname", "ZA", "Urlaub"])
        self.apprentice_list.setRowCount(len(self.apprentices))

        for row, apprentice in enumerate(self.apprentices):
            for col, value in enumerate(apprentice):
                item = QTableWidgetItem(str(value))
                self.apprentice_list.setItem(row, col, item)

    def populate_input_fields(self, row):
        apprentice = self.apprentices[row]
        self.year_edit.setText(str(apprentice[1]))  # Lehrjahr
        self.za_edit.setText(str(apprentice[4]))  # Zeitausgleich
        self.category_edit.setText(apprentice[0])  # Beruf
        self.first_name_edit.setText(apprentice[2])  # Vorname
        self.vacation_edit.setText(str(apprentice[5]))  # Urlaub
        self.last_name_edit.setText(apprentice[3])  # Nachname

    def save_apprentice_changes(self):
        # Get the new values from the QLineEdit widgets
        new_year = self.year_edit.text()
        new_za = self.za_edit.text()
        new_category = self.category_edit.text()
        new_first_name = self.first_name_edit.text()
        new_vacation = self.vacation_edit.text()
        new_last_name = self.last_name_edit.text()

        conn = sqlite3.connect('apprentices.db') # update the database with the new values
        c = conn.cursor()
        c.execute("UPDATE Lehrlinge SET year=?, za=?, profession=?, first_name=?, vacation=?, last_name=? "
                  "WHERE rowid=1", (new_year, new_za, new_category, new_first_name, new_vacation, new_last_name))
        conn.commit()
        conn.close()

        QMessageBox.information(self, "Erfolg", "Änderungen gespeichert!")
        self.load_apprentices_from_database()  # Refresh the table widget

    def update_input_fields_from_table(self, item):
        row = item.row()
        self.populate_input_fields(row)

    def update_event_display(self):
        self.event_display.clear()
        selected_date = self.calendar.selectedDate().toString("dd/MM/yyyy")
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
