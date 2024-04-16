import sys
import sqlite3
import PyQt6.QtCore
from PyQt6.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget, QPushButton, QGroupBox, QDialog
from PyQt6.QtWidgets import QTableWidget, QHBoxLayout, QCalendarWidget, QTextBrowser, QLineEdit, QMessageBox
from PyQt6.QtWidgets import QFormLayout, QComboBox, QDialogButtonBox, QLabel, QGridLayout, QTableWidgetItem, QDateEdit
from PyQt6.QtGui import QIcon
from PyQt6.QtCore import Qt


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
        self.add_apprentice_button.clicked.connect(self.on_new_clicked)
        apprentice_layout.addWidget(self.add_apprentice_button, 0, 0)

        self.edit_apprentice_button = QPushButton(QIcon("icons/buttons/save.png"), "Bearbeiten / Speichern")
        self.edit_apprentice_button.clicked.connect(self.save_apprentice_changes)
        apprentice_layout.addWidget(self.edit_apprentice_button, 0, 1)

        self.remove_apprentice_button = QPushButton(QIcon("icons/buttons/delete.png"), "Löschen")  # delete button
        self.remove_apprentice_button.clicked.connect(self.on_delete_clicked)
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

        apprentice_layout.addWidget(QLabel("Vorname:"), 3, 0)  # first_name label and field
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
        self.search_apprentice_button.setFixedWidth(90)  # search button and search field
        self.search_apprentice_button.clicked.connect(self.on_search_clicked)
        table_layout.addWidget(self.search_apprentice_button, 0, 0, 0, 5)
        self.search_field = QLineEdit()
        self.search_field.setFixedWidth(190)
        table_layout.addWidget(self.search_field, 0, 1, 1, 0)

        self.table_sort_cb = QComboBox()
        table_layout.addWidget(self.table_sort_cb, 0, 5, 1, 1)

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
        self.vacation_button.clicked.connect(self.open_add_event_dialog)
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
        self.calendar.clicked.connect(self.update_event_display)  # update calender display

    def add_event_to_calendar(self, apprentice_name, reason, from_date, to_date):
        # create event dictionary and append to events list
        event = {
            "apprentice": apprentice_name,
            "event_type": reason,
            "date": from_date
        }
        self.events.append(event)
        self.update_event_display()  # update event display

    def load_apprentices_from_database(self):
        conn = sqlite3.connect('apprentices.db')
        c = conn.cursor()
        c.execute("SELECT profession, year, first_name, last_name, za, vacation "
                  "FROM Lehrlinge ORDER BY year, profession, first_name")  # order by year, profession, and last_name
        self.apprentices = c.fetchall()
        conn.close()

        self.apprentice_list.setColumnCount(6)  # populate the table widget with fetched data
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

    def update_input_fields_from_table(self, item):  # update table
        row = item.row()
        self.populate_input_fields(row)

    def update_event_display(self):  # update the event display
        self.event_display.clear()
        selected_date = self.calendar.selectedDate().toString("dd/MM/yyyy")
        events_on_date = [event for event in self.events if event["date"] == selected_date]
        if events_on_date:
            self.event_display.append(f"Ereignisse für {selected_date}:")
            for event in events_on_date:
                self.event_display.append(f"- {event['event_type']} : {event['apprentice']}")
        else:
            self.event_display.append(f"Keine Ereignisse für {selected_date}")

    def save_apprentice_changes(self):
        conn = sqlite3.connect('apprentices.db')
        c = conn.cursor()

        selected_row = self.apprentice_list.currentRow()

        if selected_row >= 0:
            first_name = self.apprentice_list.item(selected_row, 2).text().strip()
            last_name = self.apprentice_list.item(selected_row, 3).text()
            profession = self.apprentice_list.item(selected_row, 0).text()

            new_first_name = self.first_name_edit.text()
            new_last_name = self.last_name_edit.text()
            new_profession = self.category_edit.text()
            new_year = self.year_edit.text()
            new_za = self.za_edit.text()
            new_vacation = self.vacation_edit.text()

            try:
                sql_update = ("UPDATE Lehrlinge SET first_name=?, last_name=?, profession=?, year=?, za=?, vacation=? "
                              "WHERE first_name=? AND last_name=? AND profession=?")
                c.execute(sql_update, (
                    new_first_name, new_last_name, new_profession, new_year, new_za, new_vacation, first_name,
                    last_name,
                    profession))
                conn.commit()
                QMessageBox.information(self, "Erfolg", "Eintrag erfolgreich aktualisiert.")
                self.load_apprentices_from_database()  # Refresh the apprentice list
            except Exception as e:
                print(e)

    def on_delete_clicked(self):
        if self.apprentice_list.currentRow() < 0:  # check if a row is selected
            QMessageBox.warning(self, "Warnung", "Kein Eintrag ausgewählt.")
            return

        # Clear input fields after adding new apprentice
        self.first_name_edit.clear()
        self.last_name_edit.clear()
        self.category_edit.clear()
        self.year_edit.clear()
        self.za_edit.clear()
        self.vacation_edit.clear()

        selected_row = self.apprentice_list.currentRow()  # get the selected row from the table
        conn = sqlite3.connect('apprentices.db')
        c = conn.cursor()
        if selected_row >= 0:
            # get the values from the selected row that uniquely identify the record
            first_name = self.apprentice_list.item(selected_row, 2).text().strip()
            last_name = self.apprentice_list.item(selected_row, 3).text()
            profession = self.apprentice_list.item(selected_row, 0).text()
            print(first_name)
            # delete the entry from the database using the unique identifier (the green key in heidisql)
            try:
                sql_delete = ("DELETE FROM Lehrlinge WHERE first_name=\'" + first_name + "\' " "AND last_name=\'"
                              + last_name + "\' AND profession=\'" + profession + "\';")
                c.execute(sql_delete)
                conn.commit()
                QMessageBox.information(self, "Erfolg", "Eintrag erfolgreich gelöscht.")
                conn.commit()
                self.load_apprentices_from_database()  # refresh the table widget
            except Exception as e:
                print(e)

    def on_new_clicked(self):
        conn = sqlite3.connect('apprentices.db')
        c = conn.cursor()

        first_name = self.first_name_edit.text()  # fetch values from the input fields
        last_name = self.last_name_edit.text()
        profession = self.category_edit.text()
        year = self.year_edit.text()
        za = self.za_edit.text()
        vacation = self.vacation_edit.text()

        self.first_name_edit.clear()   # clear input fields after adding new apprentice
        self.last_name_edit.clear()
        self.category_edit.clear()
        self.year_edit.clear()
        self.za_edit.clear()
        self.vacation_edit.clear()

        if not (first_name or last_name or profession or year or za or vacation):  # check if all input fields are empty
            QMessageBox.warning(self, "Warnung", "Bitte füllen Sie alle Eingabefelder aus.")
            return

        # check if the apprentice already exists
        c.execute("SELECT * FROM Lehrlinge WHERE first_name=? AND last_name=? AND profession=?",
                  (first_name, last_name, profession))
        existing_apprentice = c.fetchone()

        if existing_apprentice:
            QMessageBox.warning(self, "Warnung", "Lehrling existiert bereits.")
        else:
            c.execute(  # insert the new apprentice into the database
                "INSERT INTO Lehrlinge (first_name, last_name, profession, year, za, vacation) "
                "VALUES (?, ?, ?, ?, ?, ?)",
                (first_name, last_name, profession, year, za, vacation))
            conn.commit()
            QMessageBox.information(self, "Erfolg", "Neuer Lehrling hinzugefügt.")
            self.load_apprentices_from_database()  # refresh the apprentice list

    def on_search_clicked(self):  # searches the database
        search_text = self.search_field.text().strip()
        if not search_text:
            self.load_apprentices_from_database()  # if search field is empty, load all apprentices
        else:
            conn = sqlite3.connect('apprentices.db')
            c = conn.cursor()
            c.execute("SELECT profession, year, first_name, last_name, za, vacation "
                      "FROM Lehrlinge WHERE first_name LIKE ? OR last_name LIKE ? "
                      "OR profession LIKE ? ORDER BY year, profession, last_name",
                      ('%' + search_text + '%', '%' + search_text + '%', '%' + search_text + '%'))
            self.apprentices = c.fetchall()
            conn.close()

            self.apprentice_list.setRowCount(0)  # clear the table widget
            for row, apprentice in enumerate(self.apprentices):
                self.apprentice_list.insertRow(row)
                for col, value in enumerate(apprentice):
                    item = QTableWidgetItem(str(value))
                    self.apprentice_list.setItem(row, col, item)

    def open_add_event_dialog(self):  # to call the class when button is pressed
        dialog = AddEventDialog(self)
        dialog.exec()

class AddEventDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Ereignis hinzufügen")

        main_layout = QFormLayout()

        self.apprentice_combo = QComboBox()  # combo box with apprentices
        main_layout.addRow("Lehrling:", self.apprentice_combo)

        self.reason_lineedit = QLineEdit()  # reason QLineedit
        main_layout.addRow("Grund:", self.reason_lineedit)

        self.date_from_calendar = QCalendarWidget()  # from calender
        self.date_from_calendar.setGridVisible(True)
        main_layout.addRow("Von:", self.date_from_calendar)

        self.date_to_calendar = QCalendarWidget()  # until calender
        self.date_to_calendar.setGridVisible(True)
        main_layout.addRow("Bis:", self.date_to_calendar)

        self.button_box = QDialogButtonBox(QDialogButtonBox.StandardButton.Ok | QDialogButtonBox.StandardButton.Cancel)
        main_layout.addRow(self.button_box)

        self.setLayout(main_layout)

        self.populate_apprentices()

        self.button_box.accepted.connect(self.add_event)
        self.button_box.rejected.connect(self.reject)

    def populate_apprentices(self):  # populate the combobox
        try:
            conn = sqlite3.connect('apprentices.db')
            c = conn.cursor()
            c.execute("SELECT last_name, first_name FROM Lehrlinge ORDER BY last_name")  # fetch apprentice names
            apprentices = c.fetchall()
            conn.close()
            for apprentice in apprentices:
                full_name = f"{apprentice[0]} {apprentice[1]}"
                self.apprentice_combo.addItem(full_name)
        except Exception as e:
            print("Error in populate_apprentices method:", e)

    def add_event(self):
        try:
            apprentice = self.apprentice_combo.currentText()
            reason = self.reason_lineedit.text()
            date_from = self.date_from_calendar.selectedDate().toString(Qt.DateFormat.ISODate)
            date_to = self.date_to_calendar.selectedDate().toString(Qt.DateFormat.ISODate)

            # Now you can use these variables to perform further operations, such as adding the event to the database

            self.accept()
        except Exception as e:
            print("Error in add_event method:", e)



if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = CalendarApp()
    window.show()
    sys.exit(app.exec())
