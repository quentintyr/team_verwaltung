import sys
import sqlite3
import PyQt6.QtCore
from PyQt6.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget, QPushButton, QGroupBox, QDialog
from PyQt6.QtWidgets import QTableWidget, QHBoxLayout, QCalendarWidget, QTextBrowser, QLineEdit, QMessageBox
from PyQt6.QtWidgets import QFormLayout, QComboBox, QDialogButtonBox, QLabel, QGridLayout, QTableWidgetItem, QDateEdit
from PyQt6.QtGui import QIcon, QPalette, QTextCharFormat, QTextList
from PyQt6.QtCore import Qt
from datetime import datetime, timedelta
from PyQt6.QtWidgets import QTextEdit, QDialogButtonBox, QDialogButtonBox, QListWidget, QDateTimeEdit


class CalendarApp(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Teamverwaltung")  # creating the window
        self.setGeometry(100, 100, 1280, 720)
        self.setWindowIcon(QIcon("icons/logo/logo.ico"))

        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        
        # set reason to empty string
        self.selected_reason = ""
        
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
        self.sick_button.clicked.connect(self.open_add_event_dialog)
        button_layout.addWidget(self.sick_button)

        self.compensation_button = QPushButton(QIcon("icons/buttons/compensation.png"), "Zeitausgleich")
        self.compensation_button.clicked.connect(self.open_add_event_dialog)
        button_layout.addWidget(self.compensation_button)  # time compensation button

        self.school_button = QPushButton(QIcon("icons/buttons/school.png"), "Berufsschule")  # school button
        self.school_button.clicked.connect(self.open_add_event_dialog)
        button_layout.addWidget(self.school_button)

        self.work_button = QPushButton(QIcon("icons/buttons/desk.png"), " Abteilung")
        self.work_button.clicked.connect(self.open_add_abteilung_dialog)
        button_layout.addWidget(self.work_button)

        right_layout.addLayout(button_layout)  # adding the event button layout to the right layout

        entry_button_layout = QHBoxLayout()  # event layout

        self.delete_event_button = QPushButton(QIcon("icons/buttons/delete_event.png"), "Eintrag löschen")
        entry_button_layout.addWidget(self.delete_event_button)  # Button dem Layout hinzufügen
        self.delete_event_button.clicked.connect(self.delete_event)

        self.edit_event_button = QPushButton(QIcon("icons/buttons/edit.png"), "Eintrag bearbeiten")
        entry_button_layout.addWidget(self.edit_event_button)  # edit entry button
        self.edit_event_button.clicked.connect(self.edit)

        right_layout.addLayout(entry_button_layout)  # adding the entry button layout to the right layout

        self.event_list = QListWidget()
        right_layout.addWidget(self.event_list)

        main_layout.addLayout(left_layout)  # add left and right layouts to the main layout
        main_layout.addLayout(right_layout)

        self.central_widget.setLayout(main_layout)

        self.events = []
        self.apprentices = []

        self.load_apprentices_from_database()  # Load apprentices from database
        self.update_event_display()  # Update the event display widget
        self.calendar.clicked.connect(self.update_event_display)  # update calender display

        self.event_list.itemClicked.connect(self.on_event_selected)
        
    def open_add_abteilung_dialog(self):
        dialog = AddAbteilungDialog(self)
        dialog.exec()
        
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
        self.year_edit.setText(str(apprentice[1]))
        self.za_edit.setText(str(apprentice[4]))
        self.category_edit.setText(apprentice[0])
        self.first_name_edit.setText(apprentice[2])
        self.vacation_edit.setText(str(apprentice[5]))
        self.last_name_edit.setText(apprentice[3])

    def update_event_display(self):
        selected_date = self.calendar.selectedDate().toString(Qt.DateFormat.ISODate)
        try:
            conn = sqlite3.connect('apprentices.db')
            c = conn.cursor()
            c.execute("SELECT ID, apprentice, von, bis, reason, Typ FROM Dates WHERE von<=? AND bis>=?",
                    (selected_date, selected_date))
            self.events = c.fetchall()  # Update self.events with fetched events
            conn.close()
            self.event_list.clear()
            for event in self.events:
                apprentice = event[1]
                von = event[2]
                bis = event[3]
                reason = event[4]
                item_text = f"Lehrling: {apprentice},\nVon: {von},\nBis: {bis},\nAnwesenheit: {reason}"
                self.event_list.addItem(item_text)
        except Exception as e:
            print("Fehler beim Aktualisieren des Event-Displays:", e)
            QMessageBox.critical(self, "Fehler", "Ein Fehler ist beim Aktualisieren des Event-Displays aufgetreten.")

    def edit(self):
        selected_item = self.event_list.currentItem()
        if selected_item is None:
            QMessageBox.warning(self, "Warnung", "Bitte wählen Sie ein Event aus, das bearbeitet werden soll.")
            return
        selected_items = self.event_list.selectedItems()
        if selected_items:
            selected_item = selected_items[0]
            index = self.event_list.row(selected_item)
            if index < len(self.events):
                event = self.events[index]

                apprentice, von, bis, reason = event[1], event[2], event[3], event[4]

                dialog = QDialog(self)
                dialog.setWindowTitle("Eintrag bearbeiten")
                dialog_layout = QVBoxLayout(dialog)

                form_layout = QFormLayout()

                apprentice_edit = QLineEdit(apprentice)
                von_edit = QLineEdit(von)
                bis_edit = QLineEdit(bis)
                reason_edit = QLineEdit(reason)

                form_layout.addRow("Lehrling:", apprentice_edit)
                form_layout.addRow("Von:", von_edit)
                form_layout.addRow("Bis:", bis_edit)
                form_layout.addRow("Anwesenheit:", reason_edit)

                dialog_layout.addLayout(form_layout)

                button_box = QDialogButtonBox(QDialogButtonBox.StandardButton.Save | QDialogButtonBox.StandardButton.Cancel)
                button_box.accepted.connect(dialog.accept)
                button_box.rejected.connect(dialog.reject)
                dialog_layout.addWidget(button_box)

                if dialog.exec() == QDialog.DialogCode.Accepted:
                    new_apprentice = apprentice_edit.text()
                    new_von = von_edit.text()
                    new_bis = bis_edit.text()
                    new_reason = reason_edit.text()

                    try:
                        with sqlite3.connect('apprentices.db') as conn:
                            c = conn.cursor()
                            c.execute("UPDATE Dates SET apprentice=?, von=?, bis=?, reason=? WHERE ID=?",
                                    (new_apprentice, new_von, new_bis, new_reason, event[0]))
                            conn.commit()
                            self.update_event_display()
                    except Exception as e:
                        print("Fehler beim Bearbeiten des Eintrags:", e)

    def update_input_fields_from_table(self, item):
        row = item.row()
        self.populate_input_fields(row)

    def delete_event(self):
        # Überprüfen, ob ein Element ausgewählt ist
        selected_item = self.event_list.currentItem()
        if selected_item is None:
            QMessageBox.warning(self, "Warnung", "Bitte wählen Sie ein Event aus, das gelöscht werden soll.")
            return

        # Daten des ausgewählten Events aus der Event-Liste abrufen
        event_text = selected_item.text()
        event_data = event_text.split(",\n")
        apprentice = event_data[0].split(": ")[1]
        von = event_data[1].split(": ")[1]
        bis = event_data[2].split(": ")[1]

        try:
            # Verbindung zur Datenbank herstellen und Löschvorgang durchführen
            conn = sqlite3.connect('apprentices.db')
            c = conn.cursor()
            # Löschvorgang in der Datenbank durchführen
            c.execute("DELETE FROM Dates WHERE apprentice=? AND von=? AND bis=?",
                    (apprentice, von, bis))
            conn.commit()
            QMessageBox.information(self, "Erfolg", "Ihr Eintrag wurde erfolgreich gelöscht.")
            self.update_event_display()  # Event-Display aktualisieren
        except Exception as e:
            print("Fehler beim Löschen des Eintrags:", e)
        finally:
            conn.close()

    def on_event_selected(self, item):
        # Funktion für die Ereignisauswahl
        selected_text = item.text()
        print("Ausgewähltes Ereignis:", selected_text)

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
        # Überprüfen, ob eine Zeile ausgewählt ist
        if self.apprentice_list.currentRow() < 0:
            QMessageBox.warning(self, "Warnung", "Kein Eintrag ausgewählt.")
            return

        # Daten aus dem Table Widget abrufen
        selected_row = self.apprentice_list.currentRow()
        first_name = self.apprentice_list.item(selected_row, 2).text().strip()
        last_name = self.apprentice_list.item(selected_row, 3).text()
        profession = self.apprentice_list.item(selected_row, 0).text()

        # Verbindung zur Datenbank herstellen und Löschvorgang durchführen
        conn = sqlite3.connect('apprentices.db')
        c = conn.cursor()
        try:
            # Löschvorgang in der Datenbank durchführen
            c.execute("DELETE FROM Lehrlinge WHERE first_name=? AND last_name=? AND profession=?",
                    (first_name, last_name, profession))
            conn.commit()
            QMessageBox.information(self, "Erfolg", "Lehrling erfolgreich gelöscht.")
            self.load_apprentices_from_database()  # Aktualisierung des Table Widgets
        except Exception as e:
            print("Fehler beim Löschen des Lehrlings:", e)
            QMessageBox.critical(self, "Fehler", "Ein Fehler ist beim Löschen des Lehrlings aufgetreten.")
        finally:
            conn.close()

    def on_new_clicked(self):
        conn = sqlite3.connect('apprentices.db')
        c = conn.cursor()

        first_name = self.first_name_edit.text()  # fetch values from the input fields
        last_name = self.last_name_edit.text()
        profession = self.category_edit.text()
        year = self.year_edit.text()
        za = self.za_edit.text()
        vacation = self.vacation_edit.text()

        self.first_name_edit.clear()  # clear input fields after adding new apprentice
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

    def open_add_event_dialog(self):
        sender_button = self.sender()  # Get the button that triggered the signal
        selected_reason = ""

        if sender_button == self.vacation_button:
            selected_reason = "Urlaub"
        elif sender_button == self.sick_button:
            selected_reason = "Krank / Arzt"
        elif sender_button == self.compensation_button:
            selected_reason = "Zeitausgleich"
        elif sender_button == self.school_button:
            selected_reason = "Berufsschule"
        elif sender_button == self.work_button:
            selected_reason = "Abteilung"

        dialog = AddEventDialog(selected_reason, self)
        dialog.exec()


def save_dates_to_database(apprentice, reason, von, bis):
    try:
        conn = sqlite3.connect('apprentices.db')
        c = conn.cursor()
        c.execute("INSERT INTO Dates (apprentice, reason, von, bis) VALUES (?, ?, ?, ?)",
                (apprentice, reason, von, bis))
        conn.commit()
        conn.close()
        print("Datumsangaben erfolgreich in die Datenbank gespeichert.")
    except Exception as e:
        print("Fehler beim Speichern der Datumsangaben in die Datenbank:", e)

class AddEventDialog(QDialog):
    def __init__(self, selected_reason, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Ereignis hinzufügen")

        main_layout = QFormLayout()

        self.apprentice_combo = QComboBox()  # combo box with apprentices
        main_layout.addRow("Lehrling:", self.apprentice_combo)

        self.reason_lineedit = QLineEdit(selected_reason)  # reason QLineedit with initial selected_reason
        main_layout.addRow("Anwesenheit:", self.reason_lineedit)

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

        self.button_box.accepted.connect(self.add_event_and_save_to_database)
        self.button_box.rejected.connect(self.reject)

    def populate_apprentices(self):
        try:
            conn = sqlite3.connect('apprentices.db')
            c = conn.cursor()
            c.execute("SELECT last_name, first_name FROM Lehrlinge ORDER BY last_name")
            apprentices = c.fetchall()
            conn.close()
            for apprentice in apprentices:
                full_name = f"{apprentice[0]} {apprentice[1]}"
                self.apprentice_combo.addItem(full_name)
        except Exception as e:
            print("Error in populate_apprentices method:", e)

    def add_event_and_save_to_database(self):
        try:
            apprentice = self.apprentice_combo.currentText()
            reason = self.reason_lineedit.text()
            von = self.date_from_calendar.selectedDate().toString(Qt.DateFormat.ISODate)
            bis = self.date_to_calendar.selectedDate().toString(Qt.DateFormat.ISODate)
            save_dates_to_database(apprentice, reason, von, bis)
            self.accept()
            self.update_event_display()  # Event-Display aktualisieren
        except Exception as e:
            print("Error in add_event_and_save_to_database method:", e)
        
        
class AddAbteilungDialog(QDialog):
    def __init__(self, selected_reason, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Ereignis hinzufügen")

        main_layout = QFormLayout()

        self.apprentice_combo = QComboBox()  # combo box with apprentices
        main_layout.addRow("Lehrling:", self.apprentice_combo)

        self.abteilung_combo = QComboBox()  # combo box with Abteilung options
        main_layout.addRow("Abteilung:", self.abteilung_combo)

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

        self.button_box.accepted.connect(self.add_event_and_save_to_database)
        self.button_box.rejected.connect(self.reject)

        self.setLayout(main_layout)
        self.populate_abteilung()

    def populate_abteilung(self):
        try:
            conn = sqlite3.connect('apprentices.db')
            c = conn.cursor()
            c.execute("SELECT short FROM Abteilung ORDER BY short")
            abteilungen = c.fetchall()
            conn.close()
            for abteilung in abteilungen:
                self.abteilung_combo.addItem(abteilung[0])
        except Exception as e:
            print("Error in populate_abteilung method:", e)

    def populate_apprentices(self):
        try:
            conn = sqlite3.connect('apprentices.db')
            c = conn.cursor()
            c.execute("SELECT last_name, first_name FROM Lehrlinge ORDER BY last_name")
            apprentices = c.fetchall()
            conn.close()
            for apprentice in apprentices:
                full_name = f"{apprentice[0]} {apprentice[1]}"
                self.apprentice_combo.addItem(full_name)
        except Exception as e:
            print("Error in populate_apprentices method:", e)

    def add_event_and_save_to_database(self):
        try:
            apprentice = self.apprentice_combo.currentText()
            reason = self.abteilung_combo.currentText()
            von = self.date_from_calendar.selectedDate().toString(Qt.DateFormat.ISODate)
            bis = self.date_to_calendar.selectedDate().toString(Qt.DateFormat.ISODate)
            save_dates_to_database(apprentice, reason, von, bis)
            self.accept()
            self.update_event_display()  # Event-Display aktualisieren
        except Exception as e:
            print("Error in add_event_and_save_to_database method:", e)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = CalendarApp()
    window.show()
    sys.exit(app.exec())
