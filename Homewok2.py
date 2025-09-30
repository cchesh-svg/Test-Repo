import sys
from PyQt6.QtWidgets import (QMainWindow, QApplication,
    QLabel, QLineEdit, QVBoxLayout, QHBoxLayout, QWidget, QPushButton, QMessageBox
)
from PyQt6.QtCore import Qt

#2. Gui application to display electric car demand
class MainWindow(QMainWindow):

    def __init__(self):
        super(MainWindow, self).__init__()
        self.setWindowTitle("Electric Car Demand") 

        # 3. initialize lists and dictionaries, declared at the beginning
        self.yearList = []
        self.brandList = []
        self.demandDict = {}    

        # year layout
        yearLayout = QHBoxLayout()
        yearLayout.addWidget(QLabel("Year"))
        self.yearEdit = QLineEdit() # line creates space for user input, year
        yearLayout.addWidget(self.yearEdit)

        # brand layout
        brandLayout = QHBoxLayout()
        brandLayout.addWidget(QLabel("Brand"))
        self.brandEdit = QLineEdit() # line creates space for user input, brand 
        brandLayout.addWidget(self.brandEdit)

        # demand display label
        self.demandLabel = QLabel() 
        self.demandLabel.setFixedWidth(500)
        self.demandLabel.setFixedHeight(200)
        self.demandLabel.setStyleSheet("background-color: lightgreen; \
                                       border : 2px solid black; \
                                       font-size : 20px;")
        self.demandLabel.setAlignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignTop) # aligns text to top left corner

        # show demand button
        self.showDemandButton = QPushButton("Show Year and Brand Demand")
        self.showDemandButton.clicked.connect(self.show_demand)

        # show all demand button
        self.showAllDemandButton = QPushButton("Show All Year and Brand Demand")
        self.showAllDemandButton.clicked.connect(self.show_all_demand)

        # input layout (combines year, brand, and buttons)
        inputLayout = QVBoxLayout()
        inputLayout.addLayout(yearLayout)
        inputLayout.addLayout(brandLayout)
        inputLayout.addWidget(self.showDemandButton)
        inputLayout.addWidget(self.showAllDemandButton)    

        # main layout
        mainLayout = QVBoxLayout()
        mainLayout.addLayout(inputLayout)
        mainLayout.addWidget(self.demandLabel)
        mainLayout.setSpacing(20)
        mainLayout.setContentsMargins(20,20,20,20)
        
        mainLayoutWidget = QWidget()
        mainLayoutWidget.setLayout(mainLayout)   
        self.setCentralWidget(mainLayoutWidget)   

        self.initialize_window()

    # 4. Initialize the year list
    def initialize_years(self):
        local_years = [2022, 2023, 2024]
        self.yearList.clear()
        for year in local_years: # appending the local_years to the yearList
            self.yearList.append(year)

    # 5. Initialize the brand list
    def initialize_brands(self):
        local_brands = ["tesla", "rivian", "lucid", "nio"]
        self.brandList.clear()
        for brand in local_brands: # appending the local_brands to the brandList
            self.brandList.append(brand)

    # 6. Initialize the demand dictionary
    def initialize_demand(self):
        localArray = [[405, 420, 445, 430],
                      [160, 174, 152, 144],
                      [48, 42, 39, 45]]
        self.demandDict.clear() # clears dictionary
        for y in self.yearList:
            for b in self.brandList: # nested loop to go through both lists
                i = self.yearList.index(y)
                j = self.brandList.index(b)
                key = str(y) + b
                value = localArray[i][j]
                self.demandDict.update({key: value}) # updating dictionary 

    # 7. Show demand for specific year and brand
    def show_demand(self):
        try:
            year = int(self.yearEdit.text())
            if year not in self.yearList: # if year not in list, raise exception
                raise Exception("Year not found in available years")
            brand = self.brandEdit.text().lower().strip()
            if len(brand) == 0: # is length is zero, raise exception
                raise Exception("Brand name is empty")
            if brand not in self.brandList: # if brand not in list, raise exception
                raise Exception("Brand not found")
                
            key = str(year) + brand
            demand = self.demandDict[key]
            message = "The demand for " + str(year) + " " + brand + " is " + str(demand)
            self.demandLabel.setText(message)
            
        except ValueError:
            self.show_message("There is an error in year", "Error", QMessageBox.Icon.Critical)
        except Exception as e:
            self.show_message(e.args[0], 'Error', QMessageBox.Icon.Critical)

    # 8. Show all demand in tabular format
    def show_all_demand(self):
        result_string = "Brand"
        for b in self.brandList:
            result_string += '\t' + b # tab space between each brand
        for y in self.yearList:
            result_string += '\n' + str(y) # creates the column labels
            for brand in self.brandList:
                key = str(y) + brand
                value = self.demandDict[key]
                result_string += '\t' + "{:.0f}".format(value) 
        self.demandLabel.setText(result_string)


    # 9. Initialize window by calling all initialization functions from steps 4, 5, and 6
    def initialize_window(self):
        self.initialize_years()
        self.initialize_brands()
        self.initialize_demand()

    # 10. Show error message in a QMessageBox, same as lecture
    def show_message(self, txt, title, icon):
        msg = QMessageBox()
        msg.setIcon(icon)
        msg.setText(txt)
        msg.setWindowTitle(title)
        msg.setStandardButtons(QMessageBox.StandardButton.Ok | QMessageBox.StandardButton.Cancel)
        response = msg.exec()   


app = QApplication(sys.argv)
window = MainWindow()
window.show()
app.exec()