from PyQt6 import QtWidgets, uic
import sys
import sqlite3
import PyQt6.QtCore
from PyQt6.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget, QPushButton, QGroupBox, QDialog
from PyQt6.QtWidgets import QTableWidget, QHBoxLayout, QCalendarWidget, QTextBrowser, QLineEdit, QMessageBox
from PyQt6.QtWidgets import QFormLayout, QComboBox, QDialogButtonBox, QLabel, QGridLayout, QTableWidgetItem, QDateEdit
from PyQt6.QtGui import QIcon, QPalette, QTextCharFormat, QTextList
from PyQt6.QtCore import Qt, QDate
from datetime import datetime, timedelta
from PyQt6.QtWidgets import QTextEdit, QDialogButtonBox, QDialogButtonBox, QListWidget, QDateTimeEdit

class CalenderApp(QtWidgets.QMainWindow):
    def __init__(self):
        super(CalenderApp, self).__init__()   # call the inherited classes __init__ method
        uic.loadUi('ui/calender_ui.ui', self)   # load the ui file
        self.show()

        # main window settings
        self.setWindowTitle("Teamverwaltung")
        self.setWindowIcon(QIcon("icons/logo/team.gif"))

        # set the groupBox names
        self.apprentice_groupBox.setTitle("Lehrlinge")
        self.table_groupBox.setTitle("Tabelle")

        # set icons and the text for the apprentice buttons
        self.add_apprentice_button.setIcon(QIcon("icons/buttons/new.ico"))  # add apprentice
        self.add_apprentice_button.setText("Hinzufügen")
        
        self.delete_apprentice_button.setIcon(QIcon("icons/buttons/delete.png"))  # delete apprentice
        self.delete_apprentice_button.setText("Löschen")

        self.edit_apprentice_button.setIcon(QIcon("icons/buttons/save.png"))  # save & edit apprentice
        self.edit_apprentice_button.setText("Bearbeiten / Speichern")

        # set the labels for the input fields
        self.year_label.setText("Lehrjahr")
        self.profession_label.setText("Beruf")
        self.first_name_label.setText("Vorname")
        self.last_name_label.setText("Nachname")
        self.time_label.setText("Zeitausgleich")
        self.vacation_label.setText("Urlaub")

        # search button and combo box
        self.search_button.setIcon(QIcon("icons/buttons/search.png"))
        self.search_button.setText("Suchen")

        self.sort_comboBox.addItems(["Lehrlinge", "Abteilungen", "Archiv"])

        # set icons and text for the events
        self.vacation_button.setIcon(QIcon("icons/buttons/vacation.png"))  # vacation button
        self.vacation_button.setText("Urlaub")

        self.time_button.setIcon(QIcon("icons/buttons/compensation.png"))  # time compensation button
        self.time_button.setText("Zeitausgleich")

        self.sick_button.setIcon(QIcon("icons/buttons/sick.png"))  # sick leave button
        self.sick_button.setText("Krank / Arzt")

        self.school_button.setIcon(QIcon("icons/buttons/school.png"))  # vocational school button
        self.school_button.setText("Berufsschule")

        self.department_button.setIcon(QIcon("icons/buttons/desk.png"))  # department button
        self.department_button.setText("Abteilung")

        # edit / delete event button
        self.delete_event_button.setIcon(QIcon("icons/buttons/delete_event.png"))  # delete event button
        self.delete_event_button.setText("Eintrag löschen")

        self.edit_event_button.setIcon(QIcon("icons/buttons/edit.png"))  # edit event button
        self.edit_event_button.setText("Eintrag bearbeiten")
        
        # connections to the buttons
        self.add_apprentice_button.clicked.connect(self.on_new_clicked)
        self.search_button.clicked.connect(self.on_search_clicked)
        self.edit_apprentice_button.clicked.connect(self.save_apprentice_changes)
        self.delete_apprentice_button.clicked.connect(self.on_delete_clicked)
        # event connection buttons   
        self.vacation_button.clicked.connect(self.open_add_event_dialog)
        self.sick_button.clicked.connect(self.open_add_event_dialog)
        self.time_button.clicked.connect(self.open_add_event_dialog)
        self.school_button.clicked.connect(self.open_add_event_dialog)
        self.department_button.clicked.connect(self.open_add_abteilung_dialog)
        self.delete_event_button.clicked.connect(self.delete_event)
        self.edit_event_button.clicked.connect(self.edit)   
        
        self.events = []
        self.apprentices = []

        self.sort_comboBox.currentIndexChanged.connect(self.on_combobox_changed) # check for current index from comboBox
        self.calendar.clicked.connect(self.update_event_display)  # update calender display

        self.apprentice_list.cellClicked.connect(self.update_input_fields_from_table) # fill qlineedit when cell clicked
        self.event_list.itemClicked.connect(self.on_event_selected)

        # updates
        self.update_event_display()  # Update the event display widget
        self.load_apprentices_from_database() # Load apprentices from database

    def on_combobox_changed(self):
        current_text = self.sort_comboBox.currentText()
        if current_text == "Lehrlinge":
            self.load_apprentices_from_database()
            self.apprentice_list.cellClicked.connect(self.update_input_fields_from_table)  # Ensure connection
        else:
            self.apprentice_list.cellClicked.disconnect(self.update_input_fields_from_table)  # Disconnect for other views
            self.first_name_edit.clear()  # clear input fields after adding new apprentice
            self.last_name_edit.clear()
            self.category_edit.clear()
            self.year_edit.clear()
            self.time_edit.clear()
            self.vacation_edit.clear()
        if current_text == "Abteilungen":
            self.load_department_from_database()
            
        # TODO - ADD | automatic funtion that archives apprentices
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

        # Set column widths
        self.apprentice_list.setColumnWidth(0, 70)  # Beruf
        self.apprentice_list.setColumnWidth(1, 50)  # Lehrjahr
        self.apprentice_list.setColumnWidth(2, 120)  # Vorname
        self.apprentice_list.setColumnWidth(3, 150)  # Nachname
        self.apprentice_list.setColumnWidth(4, 100)  # ZA
        self.apprentice_list.setColumnWidth(5, 100)  # Urlaub

    def load_department_from_database(self):
        conn = sqlite3.connect('apprentices.db')
        c = conn.cursor()
        c.execute("SELECT name, short, leader "
                "FROM Abteilung ORDER BY name, short, leader ")  # order by year, profession, and last_name
        self.department = c.fetchall()
        conn.close()

        self.apprentice_list.setColumnCount(3)  # populate the table widget with fetched data
        self.apprentice_list.setHorizontalHeaderLabels(["Abteilungsname", "Kürzel", "Abteilungsleiter"])
        self.apprentice_list.setRowCount(len(self.department))

        for row, department in enumerate(self.department):
            for col, value in enumerate(department):
                item = QTableWidgetItem(str(value))
                self.apprentice_list.setItem(row, col, item)

        self.apprentice_list.setColumnWidth(0, 220)
        self.apprentice_list.setColumnWidth(1, 220)
        self.apprentice_list.setColumnWidth(2, 150)

    def populate_input_fields(self, row):
        apprentice = self.apprentices[row]
        self.year_edit.setText(str(apprentice[1]))
        self.time_edit.setText(str(apprentice[4]))
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

    def update_input_fields_from_table(self, row, column):
        if self.sort_comboBox.currentText() == "Lehrlinge":
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
            new_za = self.time_edit.text()
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
        za = self.time_edit.text()
        vacation = self.vacation_edit.text()

        self.first_name_edit.clear()  # clear input fields after adding new apprentice
        self.last_name_edit.clear()
        self.category_edit.clear()
        self.year_edit.clear()
        self.time_edit.clear()
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
        current_text = self.sort_comboBox.currentText()
        # apprentice search
        if current_text == "Lehrlinge":
            search_text = self.search_edit.text().strip()
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
        # department search
        if current_text == "Abteilungen":
            search_text = self.search_edit.text().strip()
            if not search_text:
                self.load_department_from_database()  # if search field is empty, load all apprentices
            else:
                conn = sqlite3.connect('apprentices.db')
                c = conn.cursor()
                c.execute("SELECT name, short, leader "
                        "FROM ABTEILUNG WHERE name LIKE ? OR short LIKE ? "
                        "OR leader LIKE ? ORDER BY name, short, leader",
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
        elif sender_button == self.time_button:
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
        self.setWindowTitle("Abwesenheit hinzufügen")
        self.setWindowIcon(QIcon("icons/logo/team.gif"))

        main_layout = QFormLayout()

        self.apprentice_combo = QComboBox()  # combo box with apprentices
        main_layout.addRow("Lehrling:", self.apprentice_combo)

        self.reason_lineedit = QLineEdit(selected_reason)  # reason QLineedit with initial selected_reason
        main_layout.addRow("Anwesenheit:", self.reason_lineedit)

        self.date_from_calendar = QDateEdit()  # from calendar
        self.date_from_calendar.setCalendarPopup(True)
        self.date_from_calendar.setDate(QDate.currentDate())
        self.date_from_calendar.setStyleSheet("""
            QDateEdit::drop-down {
                border-left-width: 1px;
                border-left-color: darkgray;
                border-left-style: solid; /* just a single line */
                background-color: #D3D3D3;
            }

            QDateEdit::down-arrow {
                image: url(icons/buttons/calendar.png); /* path to your calendar icon */
                width: 12px; /* Adjust the width of the icon */
                height: 12px; /* Adjust the height of the icon */
                
            }
        """)
        main_layout.addRow("Von:", self.date_from_calendar)

        self.date_to_calendar = QDateEdit()  # from calendar
        self.date_to_calendar.setCalendarPopup(True)
        self.date_to_calendar.setDate(QDate.currentDate())
        self.date_to_calendar.setStyleSheet("""
            QDateEdit::drop-down {
                border-left-width: 1px;
                border-left-color: darkgray;
                border-left-style: solid; /* just a single line */
                background-color: #D3D3D3;
            }

            QDateEdit::down-arrow {
                image: url(icons/buttons/calendar.png); /* path to your calendar icon */
                width: 12px; /* Adjust the width of the icon */
                height: 12px; /* Adjust the height of the icon */
                
            }
        """)
        main_layout.addRow("Bis:", self.date_to_calendar)

        self.button_box = QDialogButtonBox(QDialogButtonBox.StandardButton.Ok | QDialogButtonBox.StandardButton.Cancel)
        main_layout.addRow(self.button_box)

        self.setLayout(main_layout)
        self.populate_apprentices() # TODO - ADD | archive for apprentice that completed apprenticeship

        self.button_box.accepted.connect(self.add_event_and_save_to_database)
        self.button_box.rejected.connect(self.reject)

    # TODO - ADD | Button to display archived apprentices
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
        
        
from PyQt6.QtWidgets import QDialog, QFormLayout, QComboBox, QLineEdit, QDateEdit, QCalendarWidget, QDialogButtonBox
from PyQt6.QtGui import QIcon
from PyQt6.QtCore import Qt

class AddAbteilungDialog(QDialog):
    def __init__(self, selected_reason, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Einteilung der Abteilung")
        self.setWindowIcon(QIcon("icons/logo/team.gif"))

        main_layout = QFormLayout()

        self.apprentice_combo = QComboBox()  # combo box with apprentices
        main_layout.addRow("Lehrling:", self.apprentice_combo)

        self.abteilungShort = QComboBox()  # combo box with Abteilung options
        main_layout.addRow("Abteilungskürzel:", self.abteilungShort)
        
        self.abteilung = QLineEdit()  # combo box with Abteilung options
        main_layout.addRow("Abteilungname:", self.abteilung)
        self.abteilung.setDisabled(True)

        self.date_from_calendar = QDateEdit()  # from calendar
        self.date_from_calendar.setCalendarPopup(True)
        self.date_from_calendar.setDate(QDate.currentDate())
        self.date_from_calendar.setStyleSheet("""
            QDateEdit::drop-down {
                border-left-width: 1px;
                border-left-color: darkgray;
                border-left-style: solid; /* just a single line */
                background-color: #D3D3D3;
            }

            QDateEdit::down-arrow {
                image: url(icons/buttons/calendar.png); /* path to your calendar icon */
                width: 12px; /* Adjust the width of the icon */
                height: 12px; /* Adjust the height of the icon */
                
            }
        """)
        main_layout.addRow("Von:", self.date_from_calendar)

        self.date_to_calendar = QDateEdit()  # from calendar
        self.date_to_calendar.setCalendarPopup(True)
        self.date_to_calendar.setDate(QDate.currentDate())
        self.date_to_calendar.setStyleSheet("""
            QDateEdit::drop-down {
                border-left-width: 1px;
                border-left-color: darkgray;
                border-left-style: solid; /* just a single line */
                background-color: #D3D3D3;
            }

            QDateEdit::down-arrow {
                image: url(icons/buttons/calendar.png); /* path to your calendar icon */
                width: 12px; /* Adjust the width of the icon */
                height: 12px; /* Adjust the height of the icon */
                
            }
        """)
        main_layout.addRow("Bis:", self.date_to_calendar)

        self.button_box = QDialogButtonBox(QDialogButtonBox.StandardButton.Ok | QDialogButtonBox.StandardButton.Cancel)
        main_layout.addRow(self.button_box)

        self.setLayout(main_layout)
        self.populate_abteilung()
        self.populate_apprentices()

    def populate_abteilung(self):
        try:
            conn = sqlite3.connect('apprentices.db')
            c = conn.cursor()
            c.execute("SELECT short FROM Abteilung ORDER BY short")
            abteilungen = c.fetchall()
            conn.close()
            for abteilung in abteilungen:
                self.abteilungShort.addItem(abteilung[0])
        except Exception as e:
            print("Error in populate_abteilung method:", e)
            
    def populate_abteilung_name(self):
        try:
            conn = sqlite3.connect('apprentices.db')
            c = conn.cursor() # initialization for the query
            c.execute("SELECT name FROM Abteilung WHERE short = "+ self.abteilungShort.currentText() + "")
            sql_satz = c.fetchall()
            print(sql_satz)
            satz_len = len(sql_satz)
            conn.close()
            if satz_len == 0: # if 0 = no entry was found
                self.abteilung.setText('?')
            else: 
                self.abteilung.setText(sql_satz[0][0])
        except Exception as e:
            print("Error in populate_abteilung method:", e)
        
            self.INFO("Länder-KZ wird angezeigt.", "I")
            conn.close()

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