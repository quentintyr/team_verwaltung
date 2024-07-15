from PyQt6 import QtWidgets, uic
from PyQt6.QtGui import QIcon

class CalenderApp(QtWidgets.QMainWindow):
    def __init__(self):
        super(CalenderApp, self).__init__()   # call the inherited classes __init__ method
        uic.loadUi('ui/calender_ui.ui', self)   # load the ui file
        self.show()

        # main window settings
        self.setWindowTitle("Teamverwaltung")
        self.setWindowIcon(QIcon("icons/logo_rect.png"))

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


      