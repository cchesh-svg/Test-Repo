import sys
from enum import Enum
from PyQt6.QtWidgets import (
    QMainWindow, QApplication, QLabel, QLineEdit,
    QVBoxLayout, QHBoxLayout, QWidget, QPushButton, QMessageBox
)
from PyQt6.QtCore import Qt

# Step 3: Enumeration
class MemberType(Enum):
    Unknown = 0
    Child = 1
    Junior = 2
    Adult = 3
    Senior = 4

#Step 2: Create main window and initialize layouts
class MainWindow(QMainWindow):

    def __init__(self): # intializer function, called when object is created
        super(MainWindow, self).__init__()
        self.setWindowTitle("Member Entry")

    # QLineEdit Widget to enter name layout
        name_layout = QHBoxLayout()
        self.nameEdit = QLineEdit() # QLine Edit function creates user text box, name
        self.nameEdit.setFixedWidth(150)
        name_layout.addWidget(QLabel("Name"))
        name_layout.addWidget(self.nameEdit)

    # QLineEdit Widget to enter age layout
        age_layout = QHBoxLayout()
        self.ageEdit = QLineEdit() # QLine Edit function creates user text box, age
        self.ageEdit.setFixedWidth(150)
        age_layout.addWidget(QLabel("Age"))
        age_layout.addWidget(self.ageEdit)

    # data entry layout, button
        data_layout = QVBoxLayout() # vertical layout
        self.enterButton = QPushButton("Enter") # 'Enter' button at bottom of interface
        self.enterButton.clicked.connect(self.enter_data) # when clicked, it calls enter_data function
        data_layout.addLayout(name_layout)
        data_layout.addLayout(age_layout)
        data_layout.addStretch()
        data_layout.addWidget(self.enterButton)
        data_layout.setSpacing(20)

    # label for displaying data
        self.dataLabel = QLabel() # creates label to display data
        self.dataLabel.setFixedWidth(250) # sets width
        self.dataLabel.setFixedHeight(200) # sets height
        self.dataLabel.setStyleSheet("border : 2px solid black;")
        self.dataLabel.setWordWrap(True)
        self.dataLabel.setAlignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignTop)

    # main layout setup
        main_layout = QHBoxLayout() # horizontal box layout
        main_layout.addLayout(data_layout)
        main_layout.addWidget(self.dataLabel)
        main_layout.setSpacing(20)
        layoutWidget = QWidget()
        layoutWidget.setLayout(main_layout)   
        self.setCentralWidget(layoutWidget)


    # Step 4: Get Member Type for each age range, return as a string rather than enum
    def MemberType(self, age):
        if age >= 0 and age < 12:
            return MemberType.Child.name
        elif age >= 13 and age < 18:
            return MemberType.Junior.name
        elif age >= 19 and age < 64:
            return MemberType.Adult.name
        elif age >= 65:
            return MemberType.Senior.name
        else:
            return MemberType.Unknown.name

    # Step 5: Initialize inputs
    def initialize_input(self):
        self.nameEdit.setText(None)
        self.ageEdit.setText(None)
        self.nameEdit.setFocus()

    # Step 6: Show message box
    def show_message(self, txt, title, icon):
        msg = QMessageBox()
        msg.setIcon(icon)
        msg.setText(txt)
        msg.setWindowTitle(title)
        msg.setStandardButtons(QMessageBox.StandardButton.Ok | QMessageBox.StandardButton.Cancel)
        response = msg.exec()

    # Step 7: Check name, raise exception if empty 
    def check_name(self):
        try: 
            if len(self.nameEdit.text()) == 0:
                raise Exception('Missing name.')
            return True
        except Exception as e:
            self.show_message(e.args[0], 'Error', QMessageBox.Icon.Critical)
            self.nameEdit.setFocus()
            return False

    # Step 8: Check age, raise exceptions, return flag and age 
    def check_age(self):
        age = None
        try:
            age = int(self.ageEdit.text()) # possible ValueError if user puts letters in
            if age < 0:
                raise Exception('Age should be at least 0, cannot be negative.')
            return True, age
        except ValueError as e: # handles value error 
            self.show_message('Error in age.','Error', QMessageBox.Icon.Critical)
            self.ageEdit.selectAll()
            self.ageEdit.setFocus()
            return False, age
        except Exception as e: # handles other exceptions
            self.show_message(e.args[0], 'Error', QMessageBox.Icon.Critical)
            self.ageEdit.selectAll()
            self.ageEdit.setFocus()
            return False, age

    # Step 9: Enter data, check inputs and display member type
    def enter_data(self): # this function is called when 'Enter' button is clicked
        nameEntered = self.check_name()
        if not nameEntered:
            return False
        ageParsed, age = self.check_age()
        if not ageParsed:
            return False
        
        self.dataLabel.setText(self.dataLabel.text() + self.nameEdit.text() + 
                               ', ' + self.MemberType(age) + '\n') # formatiing was changed, ', ' instead of ' is a ' to fit directions
        self.show_message(self.nameEdit.text() + ' entered.', 'Input', QMessageBox.Icon.Information)
        self.initialize_input()

app = QApplication(sys.argv)

window = MainWindow()
window.show()

app.exec() 
