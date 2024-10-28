from PyQt5.QtWidgets import QWidget, QLabel, QLineEdit, QPushButton, QVBoxLayout, QGridLayout, QMessageBox, QHBoxLayout
from PyQt5.QtCore import Qt
from bracket import Bracket
from gui.BracketWidget import BracketWindow  # Import the BracketWidget class


class TeamNamesWindow(QWidget):
    def __init__(self, num_teams, bracket):
        super().__init__()

        self.num_teams = num_teams
        self.bracket = bracket

        self.initUI()

    def initUI(self):
        # window size and title
        self.setGeometry(100, 100, 500, 400)
        self.setWindowTitle('Team Names')
        self.setStyleSheet('background-color: #2b2b2b; ')

        # main layout
        self.layout = QVBoxLayout()

        # label for input
        self.label = QLabel(f'Enter names for {self.num_teams} teams:')
        self.label.setAlignment(Qt.AlignCenter)
        self.label.setStyleSheet("font-size: 16px; font-weight: bold; padding: 10px; color: white;")
        self.layout.addWidget(self.label)

        # create a grid layout for team names
        self.gridLayout = QGridLayout()
        self.teamInputs = []

        # determine the number of columns based on the number of teams
        if self.num_teams <= 8:
            num_columns = 1
        else:
            num_columns = 2

        # create text fields dynamically for each team
        for i in range(self.num_teams):
            team_input = QLineEdit()
            team_input.setPlaceholderText(f'Team {i + 1}')
            team_input.setFixedWidth(150)
            team_input.setStyleSheet("font-size: 14px; padding: 5px; color: white;")

            # Get grid position
            row = i // num_columns
            column = i % num_columns
            
            # Create a QLabel with white text
            label = QLabel(f'Team {i + 1}:')
            label.setStyleSheet("color: white;")  # Set the label color to white

            # Add label and input to grid layout
            self.gridLayout.addWidget(label, row, column * 2, alignment=Qt.AlignRight) 
            self.gridLayout.addWidget(team_input, row, column * 2 + 1, alignment=Qt.AlignLeft)             

            self.teamInputs.append(team_input)

        # set grid layout spacing
        self.gridLayout.setHorizontalSpacing(10)
        self.gridLayout.setVerticalSpacing(10)

        # create horizontal layout to center the grid layout
        center_layout = QHBoxLayout()
        center_layout.addStretch()  
        center_layout.addLayout(self.gridLayout) 
        center_layout.addStretch()

        self.layout.addLayout(center_layout)

        # submit button
        self.submitButton = QPushButton('Submit')
        self.submitButton.setFixedWidth(100)
        self.submitButton.setStyleSheet("font-size: 14px; padding: 5px; background-color: #4CAF50; color: white;")
        self.submitButton.clicked.connect(self.submitTeamNames)
        self.layout.addWidget(self.submitButton, alignment=Qt.AlignCenter)

        self.setLayout(self.layout)

    def submitTeamNames(self):
        # get team names from the input fields
        team_names = []
        for input_field in self.teamInputs:
            team_name = input_field.text().strip()
            if team_name == "":
                msg_box = QMessageBox(self)
                msg_box.setWindowTitle('Invalid Input')
                msg_box.setText('All teams must have names.')
                msg_box.setStyleSheet("color: white; background-color: #2b2b2b;") 
                msg_box.setStandardButtons(QMessageBox.Ok)
                msg_box.exec_()
                return
            team_names.append(team_name)

        # set team names in the Bracket class
        for i, name in enumerate(team_names):
            self.bracket.setTeamNames(i, name)
        
        leftSide, rightSide = self.bracket.createBracket()


        print("Team names submitted successfully!")
        self.close()

        # Display the bracket here
        self.displayBracket(leftSide, rightSide)

    # TeamNamesWindow.py
    def displayBracket(self, leftSide, rightSide):
    # Pass the leftSide and rightSide teams to the BracketWindow for visual display
        self.bracketWidget = BracketWindow(leftSide, rightSide)  # Pass the bracket as well
        self.bracketWidget.show()
